from __future__ import annotations
from typing import Optional
from pydantic import BaseModel

from project.application.entities.music import Music
from project.domain.core.models.user_music import UserMusicModel


class UserMusic(BaseModel):
    user_id: int
    music_id: int

    @classmethod
    def from_orm(cls, model: UserMusicModel) -> UserMusic:
        return cls(
            user_id=model.user_id,
            music_id=model.music_id,
        )