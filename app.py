from flask import Flask
from flask_cors import CORS
from datetime import datetime
from flask_cognito import CognitoAuth
from env import COGNITO_REGION, COGNITO_USERPOOL_ID, COGNITO_APP_CLIENT_ID
from routes import health, me

app = Flask(__name__)

app.config.update({
    'COGNITO_REGION': COGNITO_REGION,
    'COGNITO_USERPOOL_ID': COGNITO_USERPOOL_ID,
    'COGNITO_APP_CLIENT_ID': COGNITO_APP_CLIENT_ID,

    # optional
    'COGNITO_CHECK_TOKEN_EXPIRATION': True
})

cogauth = CognitoAuth(app)
cogauth.init_app(app)
CORS(app)

@cogauth.identity_handler
def lookup_cognito_user(payload):
    """Look up user in our database from Cognito JWT payload."""
    
    # ID tokens contain 'cognito:username' in payload instead of 'username'
    if "cognito:username" in payload:
        return payload['cognito:username'] 

    return payload['username'] # TODO check with mongoDB. Should return the object of user information

app.register_blueprint(health)
app.register_blueprint(me)