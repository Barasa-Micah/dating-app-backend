from flask import Blueprint
from controllers.user_controller import get_users, send_connection_request, accept_connection_request, deny_connection_request

user_bp = Blueprint('user_bp', __name__)

user_bp.route('/', methods=['GET'])(get_users)
user_bp.route('/sendRequest', methods=['POST'])(send_connection_request)
user_bp.route('/acceptRequest', methods=['POST'])(accept_connection_request)
user_bp.route('/denyRequest', methods=['POST'])(deny_connection_request)
