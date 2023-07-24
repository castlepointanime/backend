from flask import Flask, Response, request
from flask_cors import CORS
from flask_cognito import CognitoAuth
from flasgger import Swagger
from controllers import ContractController, MeController, HealthController
from flask_restful import Api
import traceback
from time import strftime
import logging
from http import HTTPStatus
from utilities.types import FlaskResponseType
from config.env import COGNITO_REGION, COGNITO_USERPOOL_ID, COGNITO_APP_CLIENT_ID
from database import Users

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
Swagger(app)
api = Api(app)

logging.getLogger().setLevel(logging.INFO)
api.add_resource(ContractController, '/contract')
api.add_resource(MeController, "/me")
api.add_resource(HealthController, "/health")


@cogauth.identity_handler
def lookup_cognito_user(payload):
    """Look up user in our database from Cognito JWT payload."""
    user_id = payload['sub']

    # Query MongoDB
    user = Users.get_user(user_id)

    # Create user if no user exists
    if user is None:
        Users.create_user(user_id)
        user = Users.get_user(user_id)

    # Add database information to payload
    payload['database'] = user

    # ID tokens contain 'cognito:username' in payload instead of 'username'
    if "cognito:username" in payload:
        return payload['cognito:username']

    return payload['username']


@app.after_request
def after_request(response: Response) -> Response:
    timestamp = strftime('[%Y-%b-%d %H:%M]')  # TODO this is defined in multiple spots. Make robust
    logging.info('%s %s %s %s %s %s', timestamp, request.remote_addr, request.method, request.scheme, request.full_path, response.status)
    return response


@app.errorhandler(Exception)
def exceptions(e: Exception) -> FlaskResponseType:
    tb = traceback.format_exc()
    timestamp = strftime('[%Y-%b-%d %H:%M]')
    logging.error('%s %s %s %s %s 5xx INTERNAL SERVER ERROR\n%s', timestamp, request.remote_addr, request.method, request.scheme, request.full_path, tb)
    logging.error(e)
    return "Internal server error", HTTPStatus.INTERNAL_SERVER_ERROR


if __name__ == "__main__":
    app.run(debug=True)
    logging.getLogger().setLevel(logging.DEBUG)
