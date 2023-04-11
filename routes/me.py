from flask import Blueprint, jsonify
from flask_cognito import  cognito_auth_required, current_user, current_cognito_jwt, cognito_group_permissions
from flask import current_app
from utils import verify_id_token

me = Blueprint('me', __name__)

@me.route('/me', methods=["GET"])
@cognito_auth_required
def get():
    verify_id_token()

    return jsonify({
        'name': str(current_user),
        'email': str(current_cognito_jwt['email'])
    })

@me.route('/me', methods=["PATCH"])
@cognito_auth_required
def patch():
    return "ok"