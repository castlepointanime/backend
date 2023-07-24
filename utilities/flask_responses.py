from http import HTTPStatus
import json
from utilities.types import FlaskResponseType, JSONData


class FlaskResponses():

    @classmethod
    def not_implemented_yet(cls) -> FlaskResponseType:
        return json.dumps({'error': "not implemented yet"}), HTTPStatus.NOT_IMPLEMENTED

    @classmethod
    def success(cls, data: JSONData) -> FlaskResponseType:
        return data, HTTPStatus.OK
