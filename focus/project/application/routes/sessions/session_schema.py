from __future__ import annotations

from uuid import uuid4

from pydantic import BaseModel, ValidationError, Field
from typing import Optional
from project.utils.data_state import DataSuccess, DataFailedMessage, DataState


class StartSessionSchema(BaseModel):
    session_id: str = Field(default_factory=lambda: uuid4().hex)
    comment: Optional[str] = ''
    tag: str
    planned_minutes: int


    @staticmethod
    def from_request(json_data) -> DataState[StartSessionSchema]:
        try:
            return DataSuccess(StartSessionSchema(**json_data))
        except ValidationError as e:
            errors = [
                {"field": err["loc"][0],
                 "message": err["msg"]}
                for err in e.errors()
            ]
            return DataFailedMessage(f'Ошибка валидации при старте сессии: {errors}',error=e)

class StartBuddySessionsSchema(BaseModel):
    comment: Optional[str] = Field(default='', max_length=40)
    tag: str
    code: str
    planned_minutes: int

    @staticmethod
    def from_request(json_data) -> DataState[StartBuddySessionsSchema]:
        try:
            return DataSuccess(StartBuddySessionsSchema(**json_data))
        except ValidationError as e:
            errors = [
                {"field": err["loc"][0],
                 "message": err["msg"]}
                for err in e.errors()
            ]
            return DataFailedMessage(f'Ошибка валидации при старте сессии: {errors}',error=e)

class HeartbeatSchema(BaseModel):
    session_id: str


    @staticmethod
    def from_request(json_data) -> DataState[HeartbeatSchema]:
        try:
            return DataSuccess(HeartbeatSchema(**json_data))
        except ValidationError as e:
            errors = [
                {"field": err["loc"][0],
                 "message": err["msg"]}
                for err in e.errors()
            ]
            return DataFailedMessage(f'Ошибка валидации при обновлении сессии: {errors}',error=e)


class CancelSessionSchema(BaseModel):
    session_id: str
    reason_code: Optional[str]=None

    @staticmethod
    def from_request(json_data) -> DataState[CancelSessionSchema]:
        try:
            return DataSuccess(CancelSessionSchema(**json_data))
        except ValidationError as e:
            errors = [
                {"field": err["loc"][0],
                 "message": err["msg"]}
                for err in e.errors()
            ]
            return DataFailedMessage(f'Ошибка валидации при остановке сессии: {errors}',error=e)

class СompleteSessionSchema(BaseModel):
    session_id: str

    @staticmethod
    def from_request(json_data) -> DataState[CancelSessionSchema]:
        try:
            return DataSuccess(CancelSessionSchema(**json_data))
        except ValidationError as e:
            errors = [
                {"field": err["loc"][0],
                 "message": err["msg"]}
                for err in e.errors()
            ]
            return DataFailedMessage(f'Ошибка валидации при завершении сессии: {errors}',error=e)