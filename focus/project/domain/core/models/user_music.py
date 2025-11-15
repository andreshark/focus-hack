from typing import Optional, List
from sqlalchemy import Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from project.domain.core.models.music import MusicModel
from project.domain.core.models.user import UserModel
from project.utils.base_model import Base


class UserMusicModel(Base):
    __tablename__ = "user_musics"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    )
    music_id: Mapped[int] = mapped_column(
        ForeignKey("music.id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    )

    user: Mapped[UserModel] = relationship(back_populates="musics")

    def __repr__(self) -> str:
        return f"<UserMusic user_id={self.user_id} music_id={self.music_id}>"