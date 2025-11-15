# project/domain/sessions/session_dal.py
from __future__ import annotations
from datetime import datetime, date as date_type, timedelta, time as time_cls
from typing import Tuple, Dict, Any, List
from sqlalchemy import func, and_

from project.domain.core.models.user import UserModel
from project.domain.sessions.session_dal import SessionsDal
from project.utils.db_connection import connection_db
from project.utils.data_state import DataState, DataSuccess, DataFailedMessage
from project.domain.core.models.session import SessionModel  # твоя ORM-модель

# ---- хелперы окна периода ----
def _period_bounds(offset: int, period: str):
    """
    Возвращает [start, end) для периода day/week/month, без таймзоны.
    week — ISO-неделя (понедельник-воскресенье).
    """
    start = datetime.now().date()
    if period == "day":
        start = start + timedelta(days=1) * offset
        end = start + timedelta(days=1)
        return start, end

    if period == "week":
        start = datetime.combine(start - timedelta(days=start.weekday()) + timedelta(days=7) * offset, time_cls.min)
        end = start + timedelta(days=7)
        return start, end

    if period == "month":

        months = start.year * 12 + start.month + offset

        if months % 12 == 0:
            start = datetime((months - 1) // 12, 12, 1)
            end = datetime(start.year + 1, 1, 1)
        else:
            start = datetime(months // 12, months % 12, 1)
            end = datetime(start.year, start.month + 1, 1)
        return start, end

    raise ValueError("unknown period")


class StatsDal:
    @staticmethod
    def get_stats_for_period(user_id: int, period: str, offset: int) -> DataState:
        """
        Статистика за указанный период (day/week/month).
        KPI + streak (только если period=day) + bar focus + donuts (tags, reasons).
        """
        Session = connection_db()
        if not Session:
            return DataFailedMessage("Database connection error")

        start_dt, end_dt = _period_bounds(offset, period)

        with Session() as db:
            try:
                # ---- KPI ----
                # всего сессий (все статусы)
                total_q = (
                    db.query(func.count(SessionModel.id))
                    .filter(
                        and_(
                            SessionModel.user_id == user_id,
                            SessionModel.started_at >= start_dt,
                            SessionModel.started_at < end_dt,
                        )
                    )
                )
                total_sessions = int(total_q.scalar() or 0)

                # завершённые: сумма минут, count, средняя
                comp_q = (
                    db.query(
                        func.coalesce(func.sum(SessionModel.duration), 0).label("sum_min"),
                        func.count(SessionModel.id).label("cnt"),
                        func.coalesce(func.avg(SessionModel.duration), 0).label("avg_min"),
                    )
                    .filter(
                        and_(
                            SessionModel.user_id == user_id,
                            SessionModel.status == "completed",
                            SessionModel.started_at >= start_dt,
                            SessionModel.started_at < end_dt,
                        )
                    )
                )
                sum_min, comp_cnt, avg_min = comp_q.one()
                sum_min = int(sum_min or 0)
                comp_cnt = int(comp_cnt or 0)
                avg_min = float(avg_min or 0.0)
                success_rate = (comp_cnt / total_sessions) if total_sessions > 0 else 0.0

                kpi = {
                    "total_minutes": sum_min,
                    "completed_count": comp_cnt,
                    "avg_duration": round(avg_min, 2),
                    "success_rate": round(success_rate, 1),
                }

                # ---- focus bar (сумма минут завершённых по бакетам)
                # day -> по часам, week -> по дням, month -> по датам
                if period == "day":
                    bucket = func.date_trunc('hour', SessionModel.started_at)
                    label_fmt = "%H:00"
                elif period == "week":
                    bucket = func.date_trunc('day', SessionModel.started_at)
                    label_fmt = "%Y-%m-%d"
                else:  # month
                    bucket = func.date_trunc('day', SessionModel.started_at)
                    label_fmt = "%Y-%m-%d"

                bar_q = (
                    db.query(
                        bucket.label("bucket"),
                        func.coalesce(func.sum(SessionModel.duration), 0).label("minutes"),
                    )
                    .filter(
                        and_(
                            SessionModel.user_id == user_id,
                            SessionModel.status == "completed",
                            SessionModel.started_at >= start_dt,
                            SessionModel.started_at < end_dt,
                        )
                    )
                    .group_by(bucket)
                    .order_by(bucket.asc())
                )
                focus_bar: List[Dict[str, Any]] = []
                for b, mins in bar_q.all():
                    # b — datetime (обрезанный), mins — Decimal/int
                    focus_bar.append({
                        "bucket_start": b.isoformat(),
                        "label": b.strftime(label_fmt),
                        "minutes": int(mins or 0),
                    })

                # ---- donut: топ теги (по сумме минут завершённых)
                tags_q = (
                    db.query(
                        SessionModel.tag.label("tag"),
                        func.count(SessionModel.id).label("cnt"),  # <— считаем штуки, а не минуты
                    )
                    .filter(
                        and_(
                            SessionModel.user_id == user_id,
                            SessionModel.status == "completed",
                            SessionModel.started_at >= start_dt,
                            SessionModel.started_at < end_dt,
                        )
                    )
                    .group_by(SessionModel.tag)
                    .order_by(func.count(SessionModel.id).desc())
                    .limit(6)
                )

                tags = [{"tag": (t or "untagged"), "count": int(c or 0)} for t, c in tags_q.all()]

                # ---- donut: причины срывов (по count среди canceled)
                # предположим, что в модели есть column reason_code (nullable)
                reasons_q = (
                    db.query(
                        func.coalesce(SessionModel.reason_code, "").label("reason"),  # если у тебя reason_code — подставь его
                        func.count(SessionModel.id).label("cnt"),
                    )
                    .filter(
                        and_(
                            SessionModel.user_id == user_id,
                            SessionModel.status == "canceled",
                            SessionModel.started_at >= start_dt,
                            SessionModel.started_at < end_dt,
                        )
                    )
                    .group_by(func.coalesce(SessionModel.reason_code, ""))
                    .order_by(func.count(SessionModel.id).desc())
                )
                fail_reasons = [{"reason": (r or "unknown"), "count": int(c or 0)} for r, c in reasons_q.all()]

                result = {
                    "period": period,
                    "range": {
                        "start": start_dt.isoformat(),
                        "end": end_dt.isoformat(),
                    },
                    "kpi": kpi,
                    "charts": {
                        "focus_bar": focus_bar,
                        "tags": tags,
                        "fail_reasons": fail_reasons,
                    }
                }

                if period == 'day' and offset == 0:
                    best_streak = db.get(UserModel,user_id).best_streak
                    streak = SessionsDal.get_current_streak(user_id).data
                    result['best_streak'] = best_streak
                    result['current_streak'] = streak


                return DataSuccess(result)

            except Exception as e:
                return DataFailedMessage("Ошибка построения статистики", error=e)
