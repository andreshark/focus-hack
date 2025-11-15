from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, List, TYPE_CHECKING

from pydantic import BaseModel

# импорт только для тайпингов, чтобы не тянуть ORM на этапе импорта сущности
if TYPE_CHECKING:
    from project.domain.core.models.user import UserModel

from project.application.entities.user_character import UserCharacter
from project.application.entities.user_music import UserMusic


class User(BaseModel):
    id: int
    max_id: int
    act_char_id: int
    username: str
    avatar_url: Optional[str]
    coins: int
    best_streak: int
    characters: List[UserCharacter]
    musics: List[UserMusic]

    @classmethod
    def from_orm(cls, model: "UserModel") -> "User":
        return cls(
            id=model.id,
            max_id=model.max_id,
            act_char_id=model.act_char_id,  # <-- добавлено, раньше терялось
            username=model.username,
            avatar_url=model.avatar_url,
            coins=model.coins,
            best_streak=model.best_streak,
            characters=[UserCharacter.from_orm(uc) for uc in model.characters],
            musics=[UserMusic.from_orm(um) for um in model.musics],
        )
