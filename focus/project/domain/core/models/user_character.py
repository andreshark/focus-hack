from typing import TYPE_CHECKING
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from project.utils.base_model import Base

if TYPE_CHECKING:
    from project.domain.core.models.character import CharacterModel
    from project.domain.core.models.user import UserModel


class UserCharacterModel(Base):
    __tablename__ = "user_characters"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    )
    character_id: Mapped[int] = mapped_column(
        ForeignKey("characters.id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    )

    exp: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    level: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    user: Mapped["UserModel"] = relationship(back_populates="characters")

    def __repr__(self) -> str:
        return (
            f"<UserCharacter user_id={self.user_id} character_id={self.character_id} "
            f"level={self.level} exp={self.exp}>"
        )
