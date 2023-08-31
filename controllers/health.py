from flask.typing import ResponseReturnValue
from flasgger import swag_from
from .base_controller import BaseController
from utilities import FlaskResponses


class HealthController(BaseController):

    @swag_from("swagger/health/get.yaml")
    def get(self) -> ResponseReturnValue:
        return FlaskResponses().success("ok")
