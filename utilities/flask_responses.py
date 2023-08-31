from http import HTTPStatus
from flask.typing import ResponseReturnValue
from utilities.types import JSONType
import json


class FlaskResponses():

    @classmethod
    def not_implemented_yet(cls) -> ResponseReturnValue:
        return {'error': "not implemented yet"}, HTTPStatus.NOT_IMPLEMENTED

    @classmethod
    def success(cls, data: JSONType) -> ResponseReturnValue:
        return json.dumps(data), HTTPStatus.OK

    @classmethod
    def created_resource(cls, data: JSONType) -> ResponseReturnValue:
        return json.dumps(data), HTTPStatus.CREATED

    @classmethod
    def conflict(cls, data: JSONType) -> ResponseReturnValue:
        return json.dumps(data), HTTPStatus.CONFLICT

    @classmethod
    def bad_request(cls, msg: str) -> ResponseReturnValue:
        return {'error': msg}, HTTPStatus.BAD_REQUEST
