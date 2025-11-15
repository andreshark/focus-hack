from typing import Optional, List, TYPE_CHECKING

from sqlalchemy import Integer, Text, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.utils.base_model import Base

if TYPE_CHECKING:
    from project.domain.core.models.user_character import UserMusicModel

class MusicModel(Base):
    __tablename__ = "music"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    path: Mapped[str] = mapped_column(String, nullable=False)


    def __repr__(self) -> str:
        return f"<Music id={self.id} name={self.name!r}>"