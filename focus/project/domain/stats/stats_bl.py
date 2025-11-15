from project.domain.history.history_dal import HistoryDal
from project.domain.stats.stats_dal import StatsDal
from project.utils.data_state import DataState
from datetime import datetime


class StatsBl:
    @staticmethod
    def get_stats_for_period(user_id: int, period, offset) -> DataState:
        return StatsDal.get_stats_for_period(user_id, period, offset)