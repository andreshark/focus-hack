from typing import List, TYPE_CHECKING, Optional
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from project.utils.base_model import Base

if TYPE_CHECKING:
    from project.domain.core.models.user_character import UserCharacterModel

class CharacterModel(Base):
    __tablename__ = "characters"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)

    netrual_anim: Mapped[str] = mapped_column(String, nullable=False)
    win_anim: Mapped[str]     = mapped_column(String, nullable=False)
    lose_anim: Mapped[str]    = mapped_column(String, nullable=False)
    focus_anim: Mapped[str]   = mapped_column(String, nullable=False)
    preview: Mapped[str]   = mapped_column(String, nullable=False)


    def __repr__(self) -> str:
        return f"<Character id={self.id} name={self.name!r}>"
