from flask import jsonify, Response, abort
from http import HTTPStatus
from flask_restful import Resource
from flask import request
from flasgger import validate
import json
import logging

class BaseController(Resource):

    def __init__(self) -> None:
        super().__init__()

    def get_request_data(self, swagger_path: str, swagger_object_id: str) -> Response:
        """
        Gets and verifies request data
        """
        data = request.get_json()
        validate(data, swagger_object_id, swagger_path, validation_error_handler=self.error_handler)
        return data

    @classmethod
    def error_handler(cls, err, data, schema) -> None:
        """
        Error handler for flasgger
        """
        abort(Response(json.dumps({'error': str(err.message)}), status=HTTPStatus.BAD_REQUEST))