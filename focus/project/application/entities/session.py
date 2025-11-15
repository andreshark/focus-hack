from __future__ import annotations
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from project.domain.core.models.session import SessionModel

class Session(BaseModel):
    id: int
    user_id: int
    duration: int
    status: str
    started_at: datetime
    comment: Optional[str]
    tag: str

    @classmethod
    def from_orm(cls, model: SessionModel) -> Session:
        return cls(
            id=model.id,
            user_id=model.user_id,
            duration=model.duration,
            status=model.status,
            started_at=model.started_at,
            comment=model.comment,
            tag=model.tag,
        )