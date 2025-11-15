from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, ValidationError
from project.utils.data_state import DataSuccess, DataFailedMessage, DataState


class HistorySchema(BaseModel):
    date: datetime

    @staticmethod
    def from_request(json_data) -> DataState[HistorySchema]:
        try:
            return DataSuccess(HistorySchema(**json_data))
        except ValidationError as e:
            errors = [
                {"field": err["loc"][0],
                 "message": err["msg"]}
                for err in e.errors()
            ]
            return DataFailedMessage(f'Ошибка валидации истории: {errors}',error=e)
