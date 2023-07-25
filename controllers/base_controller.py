from flask import Response, abort
from http import HTTPStatus
from flask_restful import Resource
from flask import request
from flasgger import validate
import json
from typing import Dict, Any, Collection, Union
from utilities.types import JSONDict
from jsonschema.exceptions import ValidationError
import logging
from flask_cognito import cognito_auth_required, current_cognito_jwt
from time import strftime


class BaseController(Resource):

    @classmethod
    def log_debug(cls, msg: str) -> None:
        timestamp = strftime('[%Y-%b-%d %H:%M]')
        logging.debug('%s %s %s %s %s %s %s', timestamp, request.remote_addr, request.method, request.scheme, request.full_path, msg)

    @classmethod
    def get_request_data(cls, swagger_data: Union[str, dict[str, Collection[Collection[str]]]], swagger_object_id: str) -> Dict["str", Any]:
        """
        Gets and verifies request data.
        It is preferred to use a .yaml str filepath for swagger_data,
        but for dynamic swagger API's based on configs, use a dictionary of the spec
        """
        data = request.get_json()
        assert data is not None, "No data in request"
        cls.log_debug(json.dumps(data))
        if type(swagger_data) is dict:
            validate(data, swagger_object_id, specs=swagger_data, validation_error_handler=cls.error_handler)
        else:
            validate(data, swagger_object_id, swagger_data, validation_error_handler=cls.error_handler)
        return data

    @classmethod
    def _abort_request(cls, message: str, status: int) -> None:
        abort(Response(json.dumps({'error': message}), status=status))

    @classmethod
    def error_handler(cls, err: ValidationError, data: JSONDict, schema: JSONDict) -> None:
        """
        Error handler for flasgger
        """
        error_message = str(err.message)
        cls.log_debug(error_message)
        cls._abort_request(error_message, HTTPStatus.BAD_REQUEST)

    @classmethod
    @cognito_auth_required
    def verify_id_token(cls) -> None:
        """
        Returns 400 if header token is not id
        """
        if current_cognito_jwt['token_use'] != "id":
            cls._abort_request("Header must contain an ID token", HTTPStatus.BAD_REQUEST)
