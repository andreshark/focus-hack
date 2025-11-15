from __future__ import annotations
from pydantic import BaseModel

from project.domain.core.models.music import MusicModel


class Music(BaseModel):
    id: int
    name: str
    price: int
    path: str

    @classmethod
    def from_orm(cls, model: MusicModel) -> Music:
        return cls(
            id=model.id,
            name=model.name,
            price=model.price,
            path=model.path,
        )