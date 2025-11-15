from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from project.application.routes.media.media_schema import BuyMediaSchema
from project.application.routes.stats.stats_schema import StatsSchema
from project.domain.media.media_bl import MediaBl
from project.domain.stats.stats_bl import StatsBl
from project.utils.data_state import DataFailedMessage

media_router = Blueprint('media_router', __name__)

@media_router.route('/media/get_musics', methods=['GET'])
@jwt_required()
def get_all_musics():
    try:
        user_id = get_jwt_identity()
        res = MediaBl.get_all_musics(user_id = user_id)
        return res.to_response()
    except Exception as e:
        return DataFailedMessage('Ошибка получения музыки', error=e).to_response()

@media_router.route('/media/buy', methods=['POST'])
@jwt_required()
def buy_character():
    try:
        data = request.get_json()
        validate_data_state = BuyMediaSchema.from_request(data)

        if not validate_data_state:
            return validate_data_state.to_response()

        user_id = get_jwt_identity()
        res = MediaBl.buy(user_id = user_id,music_id=validate_data_state.data.music_id)
        return res.to_response()
    except Exception as e:
        return DataFailedMessage('Ошибка покупки музыки', error=e).to_response()