from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, ValidationError, field_validator
from project.utils.data_state import DataSuccess, DataFailedMessage, DataState


class BuyCharacterSchema(BaseModel):
    character_id: int

    @staticmethod
    def from_request(json_data) -> DataState[BuyCharacterSchema]:
        try:
            return DataSuccess(BuyCharacterSchema(**json_data))
        except ValidationError as e:
            errors = [
                {"field": err["loc"][0],
                 "message": err["msg"]}
                for err in e.errors()
            ]
            return DataFailedMessage(f'Ошибка валидации покупки персонажа: {errors}',error=e)

class ChangeCharacterSchema(BaseModel):
    character_id: int

    @staticmethod
    def from_request(json_data) -> DataState[BuyCharacterSchema]:
        try:
            return DataSuccess(BuyCharacterSchema(**json_data))
        except ValidationError as e:
            errors = [
                {"field": err["loc"][0],
                 "message": err["msg"]}
                for err in e.errors()
            ]
            return DataFailedMessage(f'Ошибка валидации смены персонажа: {errors}',error=e)
