from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, ValidationError, field_validator
from project.utils.data_state import DataSuccess, DataFailedMessage, DataState


class StatsSchema(BaseModel):
    period: str
    offset: int

    @field_validator('period', mode='before')
    def validate_name(cls, v):
        if not v in ['day','month','week']:
            raise ValueError('Неверная период!')
        return v

    @staticmethod
    def from_request(json_data) -> DataState[StatsSchema]:
        try:
            return DataSuccess(StatsSchema(**json_data))
        except ValidationError as e:
            errors = [
                {"field": err["loc"][0],
                 "message": err["msg"]}
                for err in e.errors()
            ]
            return DataFailedMessage(f'Ошибка валидации статистики: {errors}',error=e)
