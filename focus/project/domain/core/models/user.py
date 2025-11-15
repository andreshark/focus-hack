from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from project.utils.base_model import Base

# импортируем только для тайпингов, чтобы не создавать цикл при загрузке модулей
if TYPE_CHECKING:
    from project.domain.core.models.user_character import UserCharacterModel
    from project.domain.core.models.user_music import UserMusicModel


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    max_id: Mapped[int] = mapped_column(Text, nullable=False)
    username: Mapped[str] = mapped_column(Text, nullable=False)
    act_char_id: Mapped[int] = mapped_column(Integer, nullable=False)
    avatar_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    coins: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    best_streak: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    # строковые ссылки избегают раннего импорта зависимых моделей
    characters: Mapped[List["UserCharacterModel"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    musics: Mapped[List["UserMusicModel"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} username={self.username!r}>"
