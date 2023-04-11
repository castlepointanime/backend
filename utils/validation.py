from flask import jsonify
from flask_cognito import cognito_auth_required, current_user, current_cognito_jwt, cognito_group_permissions

def verify_id_token():
    """
    Returns 400 if header token is not id
    """
    if current_cognito_jwt['token_use'] == "id":
        return jsonify({'error': "Header must contain ID token"}), 400