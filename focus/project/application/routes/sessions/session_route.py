from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_socketio import emit, join_room, disconnect, leave_room, rooms
from loguru import logger

from project import socketio
from project.application.routes.sessions.session_schema import StartSessionSchema, HeartbeatSchema, CancelSessionSchema, \
    СompleteSessionSchema, StartBuddySessionsSchema
from project.domain.sessions.session_bl import SessionsBl
from project.utils.data_state import DataFailedMessage
from project.utils.get_jwt_from_socket import require_jwt_or_disconnect

sessions_router = Blueprint('sessions_router', __name__)

@sessions_router.route('/sessions/start', methods=['POST'])
@jwt_required()
def start_session():
    try:
        data = StartSessionSchema.from_request(request.get_json())
        if not data:
            return data.to_response()
        user_id = get_jwt_identity()

        res = SessionsBl.start(
        session_id=data.data.session_id,
        user_id=user_id,
        tag=data.data.tag,
        comment=data.data.comment,
        planned_minutes=data.data.planned_minutes
        )
        return res.to_response()
    except Exception as e:
        return DataFailedMessage('Ошибка старта', error=e).to_response()


@sessions_router.route('/sessions/heartbeat', methods=['POST'])
@jwt_required()
def heartbeat():
    try:
        data = HeartbeatSchema.from_request(request.get_json())
        if not data:
            return data.to_response()

        user_id = get_jwt_identity()
        res = SessionsBl.heartbeat(data.data.session_id, user_id)
        return res.to_response()
    except Exception as e:
        return DataFailedMessage('Ошибка heartbeat', error=e).to_response()


@sessions_router.route('/sessions/cancel', methods=['POST'])
@jwt_required()
def cancel():
    try:
        data = CancelSessionSchema.from_request(request.get_json())
        if not data:
            return data.to_response()

        user_id = get_jwt_identity()
        res = SessionsBl.cancel(data.data.session_id, user_id,data.data.reason_code)
        return res.to_response()
    except Exception as e:
        return DataFailedMessage('Ошибка cancel', error=e).to_response()


def emit_state(code: str):
    data_state = SessionsBl.snapshot_room(code)
    if not data_state:
        socketio.emit("error", data_state.to_response()[0].data, namespace="/ws")
    else:
        socketio.emit("room:state", {"room": data_state.data}, to=code, namespace="/ws")

@sessions_router.route('/sessions/complete', methods=['POST'])
@jwt_required()
def complete():
    try:
        data = СompleteSessionSchema.from_request(request.get_json())
        if not data:
            return data.to_response()

        user_id = get_jwt_identity()
        res = SessionsBl.complete(data.data.session_id, user_id)
        return res.to_response()
    except Exception as e:
        return DataFailedMessage('Ошибка complete', error=e).to_response()

@socketio.on("connect", namespace="/ws")
def on_connect():
    user_id = require_jwt_or_disconnect()
    if not user_id:
        return

    code = request.args.get("code")
    sid = request.sid
    if code:
        data_state = SessionsBl.connect_room(user_id,code,sid)
    else:
        data_state = SessionsBl.create_room(user_id,sid)

    if not data_state:
        emit("error", data_state.to_response()[0].data, namespace="/ws")
        disconnect()
        return
    code = data_state.data
    join_room(code, namespace="/ws")
    emit("connected",{"zalupa":2004}, namespace="/ws")
    emit_state(data_state.data)

@socketio.on("disconnect", namespace="/ws")
def on_buddy_leave(data):
    logger.debug('leave')
    user_id = require_jwt_or_disconnect()
    sid = request.sid
    if not user_id:
        return
    sid_rooms = [r for r in rooms(namespace="/ws") if r != sid]
    if len(sid_rooms) == 0:
        return

    code = sid_rooms[0]
    if not code:
        emit("error", {"code": "no_code"})
        return

    SessionsBl.leave_room(user_id, code)
    leave_room(code)
    disconnect()
    emit_state(code)

@socketio.on("buddy:start", namespace="/ws")
def buddy_start(data):
    user_id = require_jwt_or_disconnect()
    if not user_id:
        return

    validation_data_state = StartBuddySessionsSchema.from_request(data)
    if not validation_data_state:
        return emit("error", validation_data_state.to_response()[0].data, namespace="/ws")

    data_state = SessionsBl.buddy_start(validation_data_state.data, user_id)
    if not data_state:
        return emit("error", data_state.to_response()[0].data, namespace="/ws")

    for user_session in data_state.data:
        emit("buddy:start",{"status":"start","tag":validation_data_state.data.tag,"planned_minutes":validation_data_state.data.planned_minutes,"session_code": user_session.code},to=user_session.sid, namespace="/ws")


