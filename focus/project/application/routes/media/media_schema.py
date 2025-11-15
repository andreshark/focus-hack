from __future__ import annotations
from pydantic import BaseModel, ValidationError, field_validator
from project.utils.data_state import DataSuccess, DataFailedMessage, DataState


class BuyMediaSchema(BaseModel):
    music_id: int

    @staticmethod
    def from_request(json_data) -> DataState[BuyMediaSchema]:
        try:
            return DataSuccess(BuyMediaSchema(**json_data))
        except ValidationError as e:
            errors = [
                {"field": err["loc"][0],
                 "message": err["msg"]}
                for err in e.errors()
            ]
            return DataFailedMessage(f'Ошибка валидации покупки медиа: {errors}',error=e)
