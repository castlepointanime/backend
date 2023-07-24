from flasgger import swag_from
from .base_controller import BaseController
from utilities.types import FlaskResponseType
from utilities import FlaskResponses


class HealthController(BaseController):

    @swag_from("swagger/health/get.yaml")
    def get(self) -> FlaskResponseType:
        return FlaskResponses().success("ok")
