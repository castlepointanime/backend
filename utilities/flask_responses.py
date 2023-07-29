from http import HTTPStatus
import json
from utilities.types import FlaskResponseType, JSONType


class FlaskResponses():

    @classmethod
    def not_implemented_yet(cls) -> FlaskResponseType:
        return {'error': "not implemented yet"}, HTTPStatus.NOT_IMPLEMENTED

    @classmethod
    def success(cls, data: JSONType) -> FlaskResponseType:
        return data, HTTPStatus.OK

    @classmethod
    def created_resource(cls, data: JSONType) -> FlaskResponseType:
        return data, HTTPStatus.CREATED

    @classmethod
    def conflict(cls, data: JSONType) -> FlaskResponseType:
        return data, HTTPStatus.CONFLICT

    @classmethod
    def bad_request(cls, msg: str) -> FlaskResponseType:
        return {'error': msg}, HTTPStatus.BAD_REQUEST
