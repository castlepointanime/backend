from http import HTTPStatus
import json
from utilities.types import FlaskResponseType, JSONType


class FlaskResponses():

    @classmethod
    def not_implemented_yet(cls) -> FlaskResponseType:
        return json.dumps({'error': "not implemented yet"}), HTTPStatus.NOT_IMPLEMENTED

    @classmethod
    def success(cls, data: JSONType) -> FlaskResponseType:
        return data, HTTPStatus.OK

    @classmethod
    def created_resource(cls, data: JSONType) -> FlaskResponseType:
        return data, HTTPStatus.CREATED
