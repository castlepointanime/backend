from .base_controller import BaseController
from fastapi import status
from fastapi_cloudauth.cognito import Cognito
from fastapi.responses import JSONResponse


class HealthController(BaseController):

    def __init__(self, auth: Cognito):
        super().__init__(auth)
        self.router.add_api_route("/health", self.get, methods=["GET"])

    def get(self) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content="ok"
        )
