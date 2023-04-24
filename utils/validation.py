from flask import jsonify
from flask_cognito import cognito_auth_required, current_cognito_jwt

@cognito_auth_required
def verify_id_token():
    """
    Returns 400 if header token is not id
    """
    if current_cognito_jwt['token_use'] != "id":
        return jsonify({'error': f"Header must contain ID token"}), 400