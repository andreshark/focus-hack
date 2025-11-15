from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from project.application.routes.character.character_schema import BuyCharacterSchema, ChangeCharacterSchema
from project.application.routes.stats.stats_schema import StatsSchema
from project.domain.character.character_bl import CharacterBl
from project.domain.media.media_bl import MediaBl
from project.domain.stats.stats_bl import StatsBl
from project.utils.data_state import DataFailedMessage

character_router = Blueprint('character_router', __name__)

@character_router.route('/character/get_characters', methods=['GET'])
@jwt_required()
def get_all_characters():
    try:
        user_id = get_jwt_identity()
        res = CharacterBl.get_all_characters(user_id = user_id)
        return res.to_response()
    except Exception as e:
        return DataFailedMessage('Ошибка получения персонажей', error=e).to_response()


@character_router.route('/character/buy', methods=['POST'])
@jwt_required()
def buy_character():
    try:
        data = request.get_json()
        validate_data_state = BuyCharacterSchema.from_request(data)

        if not validate_data_state:
            return validate_data_state.to_response()

        user_id = get_jwt_identity()
        res = CharacterBl.buy(user_id = user_id,character_id=validate_data_state.data.character_id)
        return res.to_response()
    except Exception as e:
        return DataFailedMessage('Ошибка покупки персонажа', error=e).to_response()


@character_router.route('/character/change', methods=['POST'])
@jwt_required()
def change_character():
    try:
        data = request.get_json()
        validate_data_state = ChangeCharacterSchema.from_request(data)

        if not validate_data_state:
            return validate_data_state.to_response()

        user_id = get_jwt_identity()
        res = CharacterBl.change_character(user_id = user_id,character_id=validate_data_state.data.character_id)
        return res.to_response()
    except Exception as e:
        return DataFailedMessage('Ошибка покупки персонажа', error=e).to_response()

@character_router.route('/character', methods=['GET'])
@jwt_required()
def get_current_character():
    try:
        user_id = get_jwt_identity()
        res = CharacterBl.get_current_character(user_id = user_id)
        return res.to_response()
    except Exception as e:
        return DataFailedMessage('Ошибка при получении данных о текущем персонаже', error=e).to_response()