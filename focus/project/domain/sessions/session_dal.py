import ast
import time
from datetime import datetime, timedelta
from typing import Optional, Dict

from flask_socketio import leave_room, disconnect
from loguru import logger
from sqlalchemy import select
from project import settings, socketio
from project.application.entities.session import Session as SessionEntity
from project.domain.core.models.session import SessionModel
from project.domain.core.models.user import UserModel
from project.domain.core.models.user_character import UserCharacterModel
from project.utils.db_connection import connection_db, connection_redis
from project.utils.data_state import DataState, DataSuccess, DataFailedMessage

def buddy_keys(code: str) -> Dict[str, str]:
    return {
        "room":    f"buddy:{code}",
        "members": f"buddy:{code}:members",
    }

def socket_leave_room(room,sid):
    leave_room(room, sid)
    disconnect(sid)

class SessionsDal:
    @staticmethod
    def redis_start_session(start_ts, session_id: str, user_id: int, planned_minutes: int, tag: str, comment: Optional[str],room: Optional[str]='') -> DataState:
        try:
            redis_client = connection_redis()
            if not redis_client:
                return DataFailedMessage("Redis Database connection error")
            redis_client.sadd('sessions:active', session_id)
            redis_client.hset(f'session:{session_id}', mapping={
                'user_id': user_id,
                'tag': tag,
                'comment': comment,
                'start_ts': start_ts,
                'planned_minutes': planned_minutes,
                'last_hb_ts': start_ts,
                'room': room
            })
            logger.debug(f'Создана сессия {session_id}')
            return DataSuccess({"session_id": session_id})

        except Exception as e:
            return DataFailedMessage(f"Ошибка создании сессии",error=e)

    @staticmethod
    def redis_heartbeat(session_id: str, user_id: int) -> DataState:
        try:
            redis_client = connection_redis()
            if not redis_client:
                return DataFailedMessage("Redis Database connection error")

            key = f'session:{session_id}'
            if not redis_client.exists(key):
                return DataFailedMessage(f'session not found id = {session_id}', code=404)
            # проверим владельца
            sid_user = redis_client.hget(key, 'user_id')
            if sid_user != str(user_id):
                return DataFailedMessage('forbidden', code=403)
            now = int(time.time())
            redis_client.hset(key, 'last_hb_ts', now)
            logger.debug(f'heartbeat session id = {session_id}')
            return DataSuccess('updated state')
        except Exception as e:
            return DataFailedMessage(f"Ошибка обновлении сессии",error=e)

    @staticmethod
    def redis_cancel(session_id: str, user_id: int,reason_code:str=None) -> DataState:
        try:
            redis_client = connection_redis()
            if not redis_client:
                return DataFailedMessage("Redis Database connection error")

            key = f'session:{session_id}'
            if not redis_client.exists(key):
                return DataFailedMessage('session not found', code=404)
            sid_user = redis_client.hget(key, 'user_id')
            if sid_user != str(user_id):
                return DataFailedMessage('forbidden', code=403)
            start_ts = redis_client.hget(key, 'start_ts')
            now = int(time.time())
            room = redis_client.hget(key,'room')
            if room:
                leave_room_data_state = SessionsDal.leave_room(sid_user, room)
                sid = leave_room_data_state.data
                socketio.server.leave_room(room, sid, namespace="/ws")
                socketio.server.disconnect(sid, namespace="/ws")

                if leave_room_data_state:
                    snapshot_data_state = SessionsDal.snapshot_room(room)
                    if snapshot_data_state:
                        socketio.emit("room:state", {"room": snapshot_data_state.data}, to=room, namespace="/ws")

            if now - int(start_ts) > 17:
                return SessionsDal.finalize_to_db(session_id,'canceled',reason_code)
            else:
                redis_client.srem('sessions:active', session_id)
                redis_client.delete(key)
                return DataSuccess()
        except Exception as e:
            return DataFailedMessage(f"Ошибка отмены сессии",error=e)

    @staticmethod
    def complete(session_id: str, user_id: int) -> DataState[SessionEntity]:
        try:
            redis_client = connection_redis()
            if not redis_client:
                return DataFailedMessage("Redis Database connection error")

            key = f'session:{session_id}'
            sid_user = redis_client.hget(key, 'user_id')
            room = redis_client.hget(key, 'room')
            if sid_user != str(user_id) or room:
                return DataFailedMessage('forbidden', code=403)
            return SessionsDal.finalize_to_db(session_id, 'completed')
        except Exception as e:
            return DataFailedMessage(f"Ошибка завершении сессии",error=e)

    @staticmethod
    def finalize_to_db(session_id: str, status: str,reason_code:str=None) -> DataState[SessionEntity]:
            redis_client = connection_redis()
            if not redis_client:
                return DataFailedMessage("Redis Database connection error")

            key = f'session:{session_id}'
            if not redis_client.exists(key):
                return DataFailedMessage('session not found', code=404)
            data = redis_client.hgetall(key)
            # сохранение в Postgres
            Session = connection_db()
            with Session() as s:
                try:
                    sess = SessionModel(
                        user_id=data.get('user_id'),
                        tag=data.get('tag'),
                        reason_code=reason_code,
                        comment=data.get('comment'),
                        started_at=datetime.fromtimestamp(int(data.get('start_ts'))),
                        duration=data.get('planned_minutes'),
                        status=status
                    )
                    s.add(sess)
                    s.commit()

                    redis_client.srem('sessions:active', session_id)
                    redis_client.delete(key)
                    return DataSuccess(SessionEntity.from_orm(sess))
                except Exception as e:
                    s.rollback()
                    return DataFailedMessage(f"Ошибка сохранения завершенной сессии", error=e)

    @staticmethod
    def maintenance_tick():
        try:
            redis_client = connection_redis()
            if not redis_client:
                return DataFailedMessage("Redis Database connection error")


            active = list(redis_client.smembers('sessions:active'))
            for sid in active:
                key = f'session:{sid}'
                if not redis_client.exists(key):
                    redis_client.srem('sessions:active', sid)
                    continue
                h = redis_client.hgetall(key)
                last_hb = int(h.get('last_hb_ts'))
                room = h.get('room')

                # авто‑cancel по тишине
                now = int(time.time())
                logger.debug(datetime.fromtimestamp(now))
                logger.debug(datetime.fromtimestamp(last_hb))
                logger.debug((datetime.fromtimestamp(now) - datetime.fromtimestamp(last_hb)).seconds)
                logger.debug(now - last_hb)
                if now - last_hb > settings.AUTO_CANCEL_SEC:
                    logger.debug(f'Удаляем сессию {sid} со старым heartbeat')
                    SessionsDal.finalize_to_db(sid,status='canceled')  # по желанию можно НЕ писать canceled; но ТЗ разрешает хранить только завершённые. Если не нужно — закомментируйте
                    if room:
                        leave_room_data_state= SessionsDal.leave_room(h.get('user_id'),room)
                        sid = leave_room_data_state.data
                        socketio.server.leave_room(room, sid, namespace="/ws")
                        socketio.server.disconnect(sid, namespace="/ws")
                        if leave_room_data_state:
                            snapshot_data_state = SessionsDal.snapshot_room(room)
                            if snapshot_data_state:
                                socketio.emit("room:state", {"room": snapshot_data_state.data}, to=room, namespace="/ws")
                    continue

                # # нормальное завершение по времени
                # if now >= start_ts + planned:
                #     SessionsDal.finalize_to_db(sid, status='completed')
        except Exception as e:
            return DataFailedMessage(f"Ошибка в потоке проверки сессий", error=e)

    @staticmethod
    def get_current_streak(user_id: int, since_days: int = 60) -> DataState:
        """
        Текущий streak (подряд до сегодняшнего дня включительно) без таймзон.
        День считается по UTC: есть >=1 completed-сессия в этот UTC-день.
        """
        Session = connection_db()
        if not Session:
            return DataFailedMessage("Database connection error")

        with Session() as session:
            try:
                today_utc = datetime.now().date()
                now = (datetime.now() - timedelta(days=since_days))
                rows = session.execute(
                    select(SessionModel.started_at)
                    .where(
                        SessionModel.user_id == user_id,
                        SessionModel.status == 'completed',
                        SessionModel.started_at >= now,
                    )
                ).scalars().all()

                days = list(map(lambda day: day.date(), rows))
                # Идём от сегодня назад, пока есть непрерывность
                streak, day = 0, today_utc
                while day in days:
                    streak += 1
                    day -= timedelta(days=1)
                return DataSuccess(streak)

            except Exception as e:
                session.rollback()
                return DataFailedMessage(f"Ошибка при получении streak",error=e)

    @staticmethod
    def give_rewards(user_id, streak, duration, quorum=0) -> DataState:
        Session = connection_db()
        if not Session:
            return DataFailedMessage("Database connection error")

        with Session() as session:
            try:
                user = session.get(UserModel,user_id)
                time_coef = duration / 25
                earned_coins = round(50 * time_coef * (1 + streak * 0.12) * (1 + quorum * 0.2))
                earned_xp = round(110 * time_coef * (1 + streak * 0.12) * (1 + quorum * 0.2))
                user.coins = user.coins + earned_coins
                user.best_streak = streak if user.best_streak < streak else user.best_streak

                user_character = session.get(UserCharacterModel, (int(user_id), user.act_char_id))
                max_level_xp = 250 * (1.2 ** user_character.level)
                current_xp = user_character.exp + earned_xp
                if current_xp > max_level_xp:
                    user_character.level = user_character.level + 1
                    user_character.exp =  current_xp - max_level_xp
                    max_level_xp = 250 * (1.2 ** user_character.level)
                else:
                    user_character.exp = current_xp

                session.commit()

                logger.debug(f"Пользователь {user.username} с ID: заработал {earned_coins} монет и получил {earned_xp} опыта")
                return DataSuccess({'earned_xp': earned_xp,'earned_coins': earned_coins,'current_level': user_character.level, 'current_xp': user_character.exp,'max_level_xp': max_level_xp, 'current_coins': user.coins})
            except Exception as e:
                session.rollback()
                return DataFailedMessage(f"Ошибка при начислении наград",error=e)

    @staticmethod
    def create_room(user_id: int, code: str,profile_data: dict) -> DataState:
        try:
            redis_client = connection_redis()
            if not redis_client:
                return DataFailedMessage("Redis Database connection error")

            k = buddy_keys(code)
            redis_client.hset(k["room"], mapping={"owner_user_id": user_id,"status":"waiting"})
            redis_client.hset(k["members"],  mapping={user_id: str(profile_data)})
            logger.debug('Комната создана')
            return DataSuccess(code)
        except Exception as e:
            return DataFailedMessage(f"Ошибка при создании комнаты", error=e)

    @staticmethod
    def connect_room(profile_data: dict, code: str) -> DataState:
        try:
            redis_client = connection_redis()
            if not redis_client:
                return DataFailedMessage("Redis Database connection error")

            k = buddy_keys(code)
            if not redis_client.exists(k["room"]):
                return DataFailedMessage('Комната не найдена')

            if not redis_client.hget(k["room"], "status") != "running":
                return DataFailedMessage('Нельзя присоедениться к уже начатой сессии')

            redis_client.hset(k["members"],  mapping={profile_data['user_id']: str(profile_data)})
            logger.debug('Подключились к комнате')
            return DataSuccess(code)
        except Exception as e:
            return DataFailedMessage(f"Ошибка при подключении к комнате", error=e)

    @staticmethod
    def snapshot_room(code: str) -> DataState:
        try:
            redis_client = connection_redis()
            if not redis_client:
                return DataFailedMessage("Redis Database connection error")

            k = buddy_keys(code)
            room = redis_client.hgetall(k["room"]) if redis_client.exists(k["room"]) else {}
            members = redis_client.hgetall(k["members"]) if redis_client.exists(k["members"]) else {}

            return DataSuccess({
                "id": code,
                "status": room.get("status"),
                "owner": room.get("owner_user_id"),
                "members": [m for m in members.values()],
            })
        except Exception as e:
            return DataFailedMessage(f"Ошибка при получении снимка комнаты", error=e)

    @staticmethod
    def get_public_profile(user_id: int,sid :str):
        Session = connection_db()
        if not Session:
            return DataFailedMessage("Database connection error")

        with Session() as session:
            try:
                user = session.get(UserModel, user_id)
                if not user:
                    return DataFailedMessage('Пользователь не найден')

                return DataSuccess({'user_id': user_id, "username": user.username, "avatar_url": user.avatar_url, "act_char_id": user.act_char_id, "sid": sid})
            except Exception as e:
                return DataFailedMessage(f"Ошибка при получении общих данных о пользователе {user_id}", error=e)

    @staticmethod
    def leave_room(user_id: int, code: str) -> DataState:
        try:
            redis_client = connection_redis()
            if not redis_client:
                return DataFailedMessage("Redis Database connection error")

            k = buddy_keys(code)
            if not redis_client.exists(k["room"]):
                return DataFailedMessage('Комната не найдена')

            data = redis_client.hget(k["members"], user_id)
            sid= ast.literal_eval(data)['sid']
            redis_client.hdel(k["members"], user_id)
            if user_id == redis_client.hget(k["room"],'owner_user_id'):
                members = list(redis_client.hgetall(k["members"]).values())
                if len(members) == 0:
                    redis_client.delete(k["room"])
                    redis_client.delete(k["members"])
                    logger.debug('Комната была закрыта, из-за отсутствия участников')
                else:
                    new_owner = ast.literal_eval(members[0])
                    redis_client.hset(k["room"], mapping={"owner_user_id": new_owner['user_id']})

            logger.debug('Вышли из комнаты')
            return DataSuccess(sid)
        except Exception as e:
            return DataFailedMessage(f"Ошибка при выходе из комнаты", error=e)

    @staticmethod
    def buddy_start(user_id: int, code: str) -> DataState:
        try:
            redis_client = connection_redis()
            if not redis_client:
                return DataFailedMessage("Redis Database connection error")

            k = buddy_keys(code)
            if not redis_client.exists(k["room"]):
                return DataFailedMessage("Комната не найдена")

            owner = redis_client.hget(k["room"], "owner_user_id")
            if owner and owner != user_id:
                return DataFailedMessage("Запустить может только владелец комнаты")

            redis_client.hset(k["room"], mapping={"status": "running"})
            members = redis_client.hgetall(k["members"])
            logger.debug('В комната запущен таймер')
            return DataSuccess(list(members.values()))
        except Exception as e:
            return DataFailedMessage(f"Ошибкапри смене состояния на старт комнаты", error=e)

    @staticmethod
    def buddy_finish(code: str) -> DataState:
        try:
            redis_client = connection_redis()
            if not redis_client:
                return DataFailedMessage("Redis Database connection error")

            k = buddy_keys(code)
            if not redis_client.exists(k["room"]):
                return DataFailedMessage("Комната не найдена")

            redis_client.hset(k["room"], mapping={"status": "waiting"})
            return DataSuccess()
        except Exception as e:
            return DataFailedMessage(f"Ошибка при смене состояния на завершение комнаты", error=e)


