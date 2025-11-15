from loguru import logger

from project.application.entities.user import User
from project.domain.core.models.user import UserModel
from project.domain.core.models.user_character import UserCharacterModel
from project.domain.core.models.user_music import UserMusicModel
from project.utils.data_state import DataState, DataFailedMessage, DataSuccess
from project.utils.db_connection import connection_db


class AuthDal:
    @staticmethod
    def init(max_id, username, avatar_url) -> DataState[User]:
        Session = connection_db()
        if not Session:
            return DataFailedMessage("Database connection error")

        with Session() as session:
            try:
                user = session.query(UserModel).filter(UserModel.max_id == max_id).first()
                if not user:
                    user = UserModel(
                        max_id=max_id,
                        username=username,
                        avatar_url=avatar_url,
                    act_char_id=4)
                    session.add(user)
                    session.flush()  # Добавить начального персонажа и музыку
                    user_character = UserCharacterModel(user_id=user.id, character_id=5)
                    session.add(user_character)
                    user_character = UserCharacterModel(user_id=user.id, character_id=4)
                    session.add(user_character)
                    user_music = UserMusicModel(user_id=user.id, music_id=5)
                    session.add(user_music)
                    user_music = UserMusicModel(user_id=user.id, music_id=4)
                    session.add(user_music)
                else:
                    user.username = username
                    user.avatar_url = avatar_url

                session.commit()

                logger.debug(f"Пользователь {user.username} с ID: {user.id} зашел")
                return DataSuccess(User.from_orm(user))
            except Exception as e:
                session.rollback()
                return DataFailedMessage(f"Ошибка при добавлении пользователя",error=e)