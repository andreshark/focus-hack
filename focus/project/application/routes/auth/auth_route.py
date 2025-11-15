from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token

from project.application.entities.user import User
from project.application.routes.auth.auth_schemas import RegisterValidateSchema
from project.domain.auth.auth_bl import AuthBl
from project.utils.data_state import DataFailedMessage

auth_router = Blueprint("auth_router", __name__)

@auth_router.route("/auth/init", methods=["POST"])
def init():
    """
    Регистрация пользователей
    :param: {
        tg_id,
        tg_username,
        user_name,
        user_role
    }
    :return:
    """
    try:
        data = request.get_json()
        validate_data_state = RegisterValidateSchema.from_request(data)

        if not validate_data_state:
            return validate_data_state.to_response()

        result = validate_data_state.data
        data_state = AuthBl.init(result)
        if not data_state:
            return data_state.to_response()

        user = data_state.data
        access_token = create_access_token(identity=str(user.id))
        return jsonify({
            "access_token": access_token,
            "profile": user.model_dump()
        }), 200

    except Exception as e:
        return DataFailedMessage(f"Ошибка входе", error=e).to_response()