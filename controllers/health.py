from .base_controller import BaseController
from fastapi import status, Response
from fastapi_cloudauth.cognito import Cognito
from fastapi.responses import JSONResponse


class HealthController(BaseController):

    def __init__(self, auth: Cognito):  # type: ignore[no-any-unimported]
        super().__init__(auth)
        self.router.add_api_route("/health", self.get, methods=["GET"], response_model=None)

    def get(self) -> Response:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=None
        )
