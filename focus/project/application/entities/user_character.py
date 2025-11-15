from __future__ import annotations
from typing import Optional
from pydantic import BaseModel

from project.application.entities.character import Character
from project.domain.core.models.user_character import UserCharacterModel


class UserCharacter(BaseModel):
    user_id: int
    character_id: int
    exp: int
    level: int

    @classmethod
    def from_orm(cls, model: UserCharacterModel) -> UserCharacter:
        return cls(
            user_id=model.user_id,
            character_id=model.character_id,
            exp=model.exp,
            level=model.level,
        )