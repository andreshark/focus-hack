from datetime import datetime
from typing import Optional, List

from sqlalchemy import Integer, Text, ForeignKey, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.utils.base_model import Base

class SessionModel(Base):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id = mapped_column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    duration: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)
    reason_code: Mapped[str] = mapped_column(String, nullable=True)
    started_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    comment: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    tag: Mapped[str] = mapped_column(String, nullable=False)

    def __repr__(self) -> str:
        return f"<Session id={self.id} status={self.status!r} started_at={self.started_at}>"