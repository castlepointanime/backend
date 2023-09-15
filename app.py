from flask import Flask, Response, request
from flask_cors import CORS
from flask_cognito import CognitoAuth
from flasgger import Swagger
from controllers import ContractController, MeController, HealthController
from flask_restful import Api
from time import strftime
import logging
from utilities.types import JSONDict
from config.env import COGNITO_REGION, COGNITO_USERPOOL_ID, COGNITO_APP_CLIENT_ID
from managers import MeManager
from http import HTTPStatus
from utilities.types import FlaskResponseType
import traceback
from database import CognitoIdentityProviderWrapper

app = Flask(__name__)

print(CognitoIdentityProviderWrapper().get_user("test"))

app.config.update({
    'COGNITO_REGION': COGNITO_REGION,
    'COGNITO_USERPOOL_ID': COGNITO_USERPOOL_ID,
    'COGNITO_APP_CLIENT_ID': COGNITO_APP_CLIENT_ID,

    # optional
    'COGNITO_CHECK_TOKEN_EXPIRATION': True
})

app.config['SWAGGER'] = {
    'title': 'AADR Backend API'
}


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
def lookup_cognito_user(payload: JSONDict) -> str:
    """Look up user in our database from Cognito JWT payload."""
    assert 'sub' in payload, "Invalid Cognito JWT payload"
    user_id = payload['sub']

    me_manager = MeManager()
    user = me_manager.get_user_from_db(user_id)

    # Add database information to payload
    payload['database'] = user

    # ID tokens contain 'cognito:username' in payload instead of 'username'
    username = None
    if "cognito:username" in payload:
        username = payload['cognito:username']
    elif "username" in payload:
        username = payload['username']

    assert type(username) == str, "Invalid username"

    return username


@app.after_request
def after_request(response: Response) -> Response:
    timestamp = strftime('[%Y-%b-%d %H:%M]')  # TODO this is defined in multiple spots. Make robust
    logging.info('%s %s %s %s %s %s', timestamp, request.remote_addr, request.method, request.scheme, request.full_path, response.status)
    return response


# @app.errorhandler(Exception)  # type: ignore[type-var]
def exceptions(e: Exception) -> FlaskResponseType:
    tb = traceback.format_exc()
    timestamp = strftime('[%Y-%b-%d %H:%M]')
    logging.error('%s %s %s %s %s 5xx INTERNAL SERVER ERROR\n%s', timestamp, request.remote_addr, request.method, request.scheme, request.full_path, tb)
    logging.error(e)
    return "Internal server error", HTTPStatus.INTERNAL_SERVER_ERROR


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    app.run(debug=True, host="0.0.0.0", port=3001)
