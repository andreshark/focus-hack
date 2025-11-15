from __future__ import annotations
from pydantic import BaseModel, computed_field, ValidationError, Field

from project.utils.data_state import DataState, DataSuccess, DataFailedMessage


class RegisterValidateSchema(BaseModel):
    max_id: int
    name: str
    surname: str
    avatar_url: str = Field(default='')

    @computed_field
    def username(self) -> str:
        return f"{self.name} {self.surname}"

    @staticmethod
    def from_request(json_data) -> DataState[RegisterValidateSchema]:
        try:
            return DataSuccess(RegisterValidateSchema(**json_data))
        except ValidationError as e:
            errors = [
                {"field": err["loc"][0],
                 "message": err["msg"]}
                for err in e.errors()
            ]
            return DataFailedMessage(f'Ошибка валидации при входе: {errors}',error=e)