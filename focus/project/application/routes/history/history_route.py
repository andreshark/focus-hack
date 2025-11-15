from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from project.application.routes.history.history_schema import HistorySchema
from project.domain.history.history_bl import HistoryBl
from project.utils.data_state import DataFailedMessage

history_router = Blueprint('history_router', __name__)

@history_router.route('/history', methods=['POST'])
@jwt_required()
def start_session():
    try:
        data = HistorySchema.from_request(request.get_json())
        if not data:
            return data.to_response()
        user_id = get_jwt_identity()

        res = HistoryBl.get_history_for_day(
        user_id=user_id,
        date=data.data.date
        )
        return res.to_response()
    except Exception as e:
        return DataFailedMessage('Ошибка получения истории', error=e).to_response()

