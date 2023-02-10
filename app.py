from flask import Flask, jsonify
from flask_cors import CORS
from datetime import datetime
from flask_cognito import CognitoAuth, cognito_auth_required, current_user, current_cognito_jwt, cognito_group_permissions
from env import COGNITO_REGION, COGNITO_USERPOOL_ID, COGNITO_APP_CLIENT_ID

app = Flask(__name__)

app.config.update({
    'COGNITO_REGION': COGNITO_REGION,
    'COGNITO_USERPOOL_ID': COGNITO_USERPOOL_ID,
    'COGNITO_APP_CLIENT_ID': COGNITO_APP_CLIENT_ID,

    # optional

    'COGNITO_CHECK_TOKEN_EXPIRATION': True,
    'COGNITO_JWT_HEADER_NAME': 'X-MyApp-Authorization',
    'COGNITO_JWT_HEADER_PREFIX': 'Bearer',
})

cogauth = CognitoAuth(app)
cogauth.init_app(app)
#CORS(app)

@app.route('/')
def main():
    return jsonify(datetime.now())

@cogauth.identity_handler
def lookup_cognito_user(payload):
    """Look up user in our database from Cognito JWT payload."""
    return User.query.filter(User.cognito_username == payload['username']).one_or_none()

@app.route('/test/userAuth')
@cognito_auth_required
@cognito_group_permissions(['User'])
def test_user_auth():
    return jsonify({
        'cognito_username': current_cognito_jwt['username'],   # from cognito pool
        'user_id': current_user.id,   # from your database
    })
    
@app.route('/test/adminAuth')
@cognito_auth_required
@cognito_group_permissions(['Admin'])
def test_admin_auth():
    return jsonify({
        'cognito_username': current_cognito_jwt['username'],   # from cognito pool
        'user_id': current_user.id,   # from your database
    })
    
@app.route('/test/staffAuth')
@cognito_auth_required
@cognito_group_permissions(['Staff'])
def test_staff_auth():
    return jsonify({
        'cognito_username': current_cognito_jwt['username'],   # from cognito pool
        'user_id': current_user.id,   # from your database
    })
    