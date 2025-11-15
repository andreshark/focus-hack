from project.domain.history.history_dal import HistoryDal
from project.utils.data_state import DataState
from datetime import datetime


class HistoryBl:
    @staticmethod
    def get_history_for_day(user_id: int, date: datetime) -> DataState:
        return HistoryDal.get_history_for_day(user_id=user_id, date=date)