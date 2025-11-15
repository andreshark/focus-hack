import ast
import random
import threading
import time
import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from loguru import logger

from project import socketio
from project.application.routes.sessions.session_schema import StartBuddySessionsSchema
from project.domain.sessions.session_dal import SessionsDal
from project.utils.data_state import DataState, DataSuccess, DataFailedMessage

@dataclass
class UserSession:
    code: str
    sid: int

class SessionsBl:
    @staticmethod
    def start(session_id: str, user_id: int, planned_minutes: int,tag: str,comment: Optional[str],room: Optional[str]='') -> DataState:
        started_at = int(time.time())
        logger.debug(datetime.fromtimestamp(started_at))
        return SessionsDal.redis_start_session(started_at, session_id, user_id, planned_minutes,tag, comment,room)

    @staticmethod
    def heartbeat(session_id: str, user_id: int) -> DataState:
        return SessionsDal.redis_heartbeat(session_id, user_id)

    @staticmethod
    def cancel(session_id: str, user_id: int,reason_code:str=None) -> DataState:
        data_state = SessionsDal.redis_cancel(session_id, user_id,reason_code)
        if data_state:
            return DataSuccess('canceled')
        return data_state

    @staticmethod
    def complete(session_id: str, user_id: int) -> DataState:
        data_state = SessionsDal.complete(session_id, user_id) # добавить начисление хуйни; сделать групповуху; советы;
        if data_state:
            session = data_state.data
            steak_data_state = SessionsDal.get_current_streak(user_id)
            if not steak_data_state:
                return steak_data_state

            return SessionsDal.give_rewards(user_id,steak_data_state.data,session.duration)

        return data_state

    @staticmethod
    def maintenance_tick() -> None:
       SessionsDal.maintenance_tick()

    @staticmethod
    def create_room(user_id: int, sid: str) -> DataState:
        code = f"{random.randint(0, 9999):04d}"
        data_state = SessionsDal.get_public_profile(user_id, sid)
        if data_state:
            profile_data = data_state.data
            return SessionsDal.create_room(user_id, code,profile_data)

        return data_state

    @staticmethod
    def connect_room(user_id: int, code: str,sid: str) -> DataState:
        data_state = SessionsDal.get_public_profile(user_id, sid)
        if data_state:
            profile_data = data_state.data
            return SessionsDal.connect_room(profile_data, code)

        return data_state

    @staticmethod
    def leave_room(user_id: int, code: str) -> DataState:
        return SessionsDal.leave_room(user_id, code)

    @staticmethod
    def snapshot_room(code: str) -> DataState:
        return SessionsDal.snapshot_room(code)

    @staticmethod
    def buddy_start(result: StartBuddySessionsSchema,user_id: int) -> DataState:
        data_state = SessionsDal.buddy_start(user_id, result.code)
        if not data_state:
            return data_state

        user_sessions = []
        for user in data_state.data:
            data = ast.literal_eval(user)
            session_id = uuid.uuid4().hex
            SessionsBl.start(session_id,data['user_id'],result.planned_minutes,result.tag,result.comment, result.code)
            user_sessions.append(UserSession(session_id,data['sid']))
        SessionsBl.start_finisher_thread(result.planned_minutes, user_sessions, result.code)
        return DataSuccess(user_sessions)


    @staticmethod
    def start_finisher_thread(duration: int, user_sessions: list[UserSession], room_code):
        def worker():
            try:
                time.sleep(duration * 60)
                for user_session in user_sessions:
                    data_state = SessionsDal.finalize_to_db(user_session.code, 'completed')
                    if not data_state:
                        continue

                    session = data_state.data
                    steak_data_state = SessionsDal.get_current_streak(session.user_id)
                    if not steak_data_state:
                        continue

                    rewards_data_state = SessionsDal.give_rewards(session.user_id, steak_data_state.data,
                                                                  session.duration,len(user_sessions))
                    if not rewards_data_state:
                        continue
                    logger.debug(f'user_session.sid = {user_session.sid}')
                    socketio.start_background_task(
                        lambda sid=user_session.sid, payload=rewards_data_state.data:
                        socketio.emit("room:completed", payload, to=sid, namespace="/ws")
                    )

                data_state = SessionsDal.buddy_finish(room_code)
                if not data_state:
                    socketio.start_background_task(lambda sid=user_session.sid: socketio.emit("error", data_state.to_response()[0], to=sid, namespace="/ws"))

                data_state = SessionsDal.snapshot_room(room_code)
                if not data_state:
                    socketio.start_background_task(lambda sid=user_session.sid: socketio.emit("error", data_state.to_response()[0], to=sid, namespace="/ws"))
                else:
                    socketio.start_background_task(
                        lambda: socketio.emit("room:state", {"room": data_state.data}, to=room_code,
                                              namespace="/ws"))
                logger.debug('Групповая сессия успешно завершилась')
            except Exception as e:
                return DataFailedMessage(f"Ошибка в завершении групповой сессии", error=e)

        threading.Thread(target=worker, daemon=True).start()

