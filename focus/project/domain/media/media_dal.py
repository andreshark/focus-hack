from __future__ import annotations
from project.application.entities.music import Music
from project.application.entities.user_music import UserMusic
from project.domain.core.models.music import MusicModel
from project.domain.core.models.user import UserModel
from project.domain.core.models.user_music import UserMusicModel
from project.utils.db_connection import connection_db
from project.utils.data_state import DataState, DataSuccess, DataFailedMessage


class MediaDal:
    @staticmethod
    def get_all_musics(user_id: int) -> DataState:
        Session = connection_db()
        if not Session:
            return DataFailedMessage("Database connection error")

        with Session() as session:
            try:
                musics = session.query(MusicModel).all()
                user_musics = session.query(UserMusicModel).filter(UserMusicModel.user_id == user_id).all()
                data = {
                    "available_musics_id":list(map(lambda c: c.music_id,user_musics)),
                    "all_musics": list(map(lambda c: Music.from_orm(c).model_dump(),musics))
                }
                return DataSuccess(data)
            except Exception as e:
                return DataFailedMessage(f"Ошибка при получении музыки",error=e)

    @staticmethod
    def buy(user_id: int, music_id: int) -> DataState:
        Session = connection_db()
        if not Session:
            return DataFailedMessage("Database connection error")

        with Session() as session:
            try:
                user = session.get(UserModel, user_id)
                music = session.get(MusicModel, music_id)
                user_music = session.get(UserMusicModel, (user_id, music_id))
                if not music:
                    return DataFailedMessage(f"Такой музыки нету",code=403)
                if  user_music:
                    return DataFailedMessage(f"У вас уже есть эта музыка",code=406)
                if music.price > user.coins:
                    return DataFailedMessage(f"Недостаточно монет",code=412)

                user.coins = user.coins - music.price
                user_music = UserMusicModel(user_id=user_id,character_id=music_id)
                session.add(user_music)
                session.commit()
                return DataSuccess(UserMusic.from_orm(user_music).model_dump())
            except Exception as e:
                session.rollback()
                return DataFailedMessage(f"Ошибка при покупке музыки",error=e)