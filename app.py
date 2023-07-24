from flask import Flask, Response, request
from flask_cors import CORS
from flasgger import Swagger
from controllers import ContractController
from flask_restful import Api
import traceback
from time import strftime
import logging
from http import HTTPStatus
from utilities.types import FlaskResponseType

app = Flask(__name__)
CORS(app)
Swagger(app)
api = Api(app)

api.add_resource(ContractController, '/contract')


@app.after_request
def after_request(response: Response) -> Response:
    timestamp = strftime('[%Y-%b-%d %H:%M]')
    logging.info('%s %s %s %s %s %s', timestamp, request.remote_addr, request.method, request.scheme, request.full_path, response.status)
    return response


@app.errorhandler(Exception)
def exceptions(e: Exception) -> FlaskResponseType:
    tb = traceback.format_exc()
    timestamp = strftime('[%Y-%b-%d %H:%M]')
    logging.error('%s %s %s %s %s 5xx INTERNAL SERVER ERROR\n%s', timestamp, request.remote_addr, request.method, request.scheme, request.full_path, tb)
    logging.error(e)
    return "Internal server error", HTTPStatus.INTERNAL_SERVER_ERROR


logging.getLogger().setLevel(logging.INFO)


if __name__ == "__main__":
    app.run(debug=True)
    logging.getLogger().setLevel(logging.DEBUG)
