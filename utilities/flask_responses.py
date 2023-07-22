from typing import Dict, Tuple
from flask import Response
from http import HTTPStatus
import json

class FlaskResponses():

    @classmethod
    def not_implemented_yet(cls) -> Response:
        return json.dumps({'error': "not implemented yet"}), HTTPStatus.NOT_IMPLEMENTED

    @classmethod
    def success(cls, data: dict) -> Response:
        return data, HTTPStatus.OK
