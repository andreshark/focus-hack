from project.domain.character.character_dal import CharacterDal
from project.utils.data_state import DataState

class CharacterBl:
    @staticmethod
    def get_all_characters(user_id: int) -> DataState:
        return CharacterDal.get_all_characters(user_id)

    @staticmethod
    def get_current_character(user_id: int) -> DataState:
        return CharacterDal.get_current_character(user_id)

    @staticmethod
    def buy(user_id: int, character_id: int) -> DataState:
        return CharacterDal.buy(user_id,character_id)

    @staticmethod
    def change_character(user_id: int, character_id: int) -> DataState:
        return CharacterDal.change_character(user_id,character_id)