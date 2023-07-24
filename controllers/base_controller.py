from flask import Response, abort
from http import HTTPStatus
from flask_restful import Resource
from flask import request
from flasgger import validate
import json
from typing import Dict, Any, Collection, Union
from utilities.types import JSONData
from jsonschema.exceptions import ValidationError
import logging


class BaseController(Resource):
    
    @classmethod
    def log_debug(cls, msg: str):
        logging.debug('%s %s %s %s %s %s %s', timestamp, request.remote_addr, request.method, request.scheme, request.full_path, msg)

    def get_request_data(self, swagger_data: Union[str, dict[str, Collection[Collection[str]]]], swagger_object_id: str) -> Dict["str", Any]:
        """
        Gets and verifies request data.
        It is preferred to use a .yaml str filepath for swagger_data,
        but for dynamic swagger API's based on configs, use a dictionary of the spec
        """
        data = request.get_json()
        assert data is not None, "No data in request"
        self.log_debug(json.dumps(data))
        if type(swagger_data) is dict:
            validate(data, swagger_object_id, specs=swagger_data, validation_error_handler=self.error_handler)
        else:
            validate(data, swagger_object_id, swagger_data, validation_error_handler=self.error_handler)
        return data

    @classmethod
    def error_handler(cls, err: ValidationError, data: JSONData, schema: JSONData) -> None:
        """
        Error handler for flasgger
        """
        error_message = str(err.message)
        self.log_debug(error_message)
        abort(Response(json.dumps({'error': error_message}), status=HTTPStatus.BAD_REQUEST))
