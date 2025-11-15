from project.application.entities.user import User
from project.application.routes.auth.auth_schemas import RegisterValidateSchema
from project.domain.auth.auth_dal import AuthDal
from project.utils.data_state import DataState


class AuthBl:
    @staticmethod
    def init(data: RegisterValidateSchema) -> DataState[User]:
        return AuthDal.init(data.max_id, data.username, data.avatar_url)