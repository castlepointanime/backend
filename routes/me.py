from flask import Blueprint, jsonify
from flask_cognito import  cognito_auth_required, current_user, current_cognito_jwt, cognito_group_permissions

me = Blueprint('me', __name__)

@me.route('/me', methods=["GET"])
@cognito_auth_required
def get():
    return jsonify({
        'username': str(current_cognito_jwt['username']),
        '_id': str(current_user)
    })

@me.route('/me', methods=["PATCH"])
@cognito_auth_required
def patch():
    return "ok"