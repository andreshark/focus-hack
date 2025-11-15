from __future__ import annotations
from pydantic import BaseModel
from project.domain.core.models.character import CharacterModel


class Character(BaseModel):
    id: int
    name: str
    price: int
    netrual_anim: str
    win_anim: str
    lose_anim: str
    focus_anim: str
    preview: str

    @classmethod
    def from_orm(cls, model: CharacterModel) -> Character:
        return cls(
            id=model.id,
            name=model.name,
            price=model.price,
            netrual_anim=model.netrual_anim,
            win_anim=model.win_anim,
            lose_anim=model.lose_anim,
            focus_anim=model.focus_anim,
            preview=model.preview
        )