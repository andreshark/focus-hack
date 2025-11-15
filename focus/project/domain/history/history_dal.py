from datetime import datetime, timedelta

from sqlalchemy import and_

from project.domain.core.models.session import SessionModel
from project.utils.data_state import DataState, DataFailedMessage, DataSuccess
from project.utils.db_connection import connection_db


class HistoryDal:
    @staticmethod
    def get_history_for_day(user_id: int, date: datetime) -> DataState:
        Session = connection_db()
        if not Session:
            return DataFailedMessage("Database connection error")

        with Session() as db:
            try:
                rows = (
                    db.query(SessionModel)
                    .filter(
                        and_(
                            SessionModel.user_id == user_id,
                        SessionModel.started_at >= date,
                        SessionModel.started_at < date + timedelta(days=1),
                        )
                    )
                    .order_by(SessionModel.started_at.desc())
                    .all()
                )

                # Сформируем «плоские» элементы
                items = []
                for s in rows:
                    items.append({
                        "started_at": s.started_at,
                        "tag": s.tag,
                        "comment": s.comment or "",
                        "duration": s.duration,
                        "status": s.status,
                    })

                return DataSuccess(items)
            except Exception as e:
                return DataFailedMessage("Ошибка получения истории из БД", error=e)