from flask import Blueprint
from project.application.routes.auth.auth_route import auth_router
from project.application.routes.sessions.session_route import sessions_router
from project.application.routes.history.history_route import history_router
from project.application.routes.stats.stats_route import stats_router
from project.application.routes.media.media_route import media_router
from project.application.routes.character.character_route import character_router

all_routes = Blueprint("all_routes", __name__, url_prefix="/api")

all_routes.register_blueprint(auth_router)
all_routes.register_blueprint(sessions_router)
all_routes.register_blueprint(history_router)
all_routes.register_blueprint(stats_router)
all_routes.register_blueprint(media_router)
all_routes.register_blueprint(character_router)