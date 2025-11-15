from __future__ import annotations

from project.application.entities.character import Character
from project.application.entities.music import Music
from project.application.entities.user_character import UserCharacter
from project.domain.core.models.character import CharacterModel
from project.domain.core.models.music import MusicModel
from project.domain.core.models.user import UserModel
from project.domain.core.models.user_character import UserCharacterModel
from project.domain.core.models.user_music import UserMusicModel
from project.utils.db_connection import connection_db
from project.utils.data_state import DataState, DataSuccess, DataFailedMessage


class CharacterDal:
    @staticmethod
    def get_all_characters(user_id: int) -> DataState:
        Session = connection_db()
        if not Session:
            return DataFailedMessage("Database connection error")

        with Session() as session:
            try:
                characters = session.query(CharacterModel).all()
                user_characters = session.query(UserCharacterModel).filter(UserCharacterModel.user_id == user_id).all()
                data = {
                    "available_characters_id":list(map(lambda c: c.character_id,user_characters)),
                    "all_characters": list(map(lambda c: Character.from_orm(c).model_dump(),characters))
                }
                return DataSuccess(data)
            except Exception as e:
                return DataFailedMessage(f"Ошибка при получении персонажей",error=e)

    @staticmethod
    def get_current_character(user_id: int) -> DataState:
        Session = connection_db()
        if not Session:
            return DataFailedMessage("Database connection error")

        with Session() as session:
            try:
                user = session.get(UserModel, user_id)
                user_character = session.get(UserCharacterModel, (user_id, user.act_char_id))
                data = {
                    "act_char_id": user.act_char_id,
                    "character_info": {"exp":user_character.exp,"level": user_character.level, "max_xp":250 * (1.2 ** user_character.level)}
                }
                return DataSuccess(data)
            except Exception as e:
                return DataFailedMessage(f"Ошибка при получении текущего персонажа",error=e)

    @staticmethod
    def buy(user_id: int, character_id: int) -> DataState:
        Session = connection_db()
        if not Session:
            return DataFailedMessage("Database connection error")

        with Session() as session:
            try:
                user = session.get(UserModel, user_id)
                character = session.get(CharacterModel, character_id)
                user_char = session.get(UserCharacterModel, (user_id, character_id))
                if not character:
                    return DataFailedMessage(f"Такого персонажа нету",code=403)
                if  user_char:
                    return DataFailedMessage(f"У вас уже есть этот персонаж",code=406)
                if character.price > user.coins:
                    return DataFailedMessage(f"Недостаточно монет",code=412)

                user.coins = user.coins - character.price
                user_char = UserCharacterModel(user_id=user_id,character_id=character_id)
                session.add(user_char)
                session.commit()
                return DataSuccess(UserCharacter.from_orm(user_char).model_dump())
            except Exception as e:
                session.rollback()
                return DataFailedMessage(f"Ошибка при покупке персонажа",error=e)

    @staticmethod
    def change_character(user_id: int, character_id: int) -> DataState:
        Session = connection_db()
        if not Session:
            return DataFailedMessage("Database connection error")

        with Session() as session:
            try:
                user = session.get(UserModel, user_id)
                character = session.get(CharacterModel, character_id)
                user_char = session.get(UserCharacterModel, (user_id, character_id))
                if not character:
                    return DataFailedMessage(f"Такого персонажа нету",code=403)
                if not user_char:
                    return DataFailedMessage(f"У вас нету этого персонажа",code=403)

                user.act_char_id = character_id
                session.commit()
                return DataSuccess('Персонаж успешно сменен')
            except Exception as e:
                session.rollback()
                return DataFailedMessage(f"Ошибка при смене персонажа",error=e)