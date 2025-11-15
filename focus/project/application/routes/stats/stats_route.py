from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from project.application.routes.stats.stats_schema import StatsSchema
from project.domain.stats.stats_bl import StatsBl
from project.utils.data_state import DataFailedMessage

stats_router = Blueprint('stats_router', __name__)

@stats_router.route('/stats', methods=['POST'])
@jwt_required()
def get_stats_for_period():
    try:
        data = StatsSchema.from_request(request.get_json())
        if not data:
            return data.to_response()

        user_id = get_jwt_identity()
        res = StatsBl.get_stats_for_period(
        period=data.data.period,
        user_id=user_id,
        offset=data.data.offset,
        )
        return res.to_response()
    except Exception as e:
        return DataFailedMessage('Ошибка получения статистики', error=e).to_response()

