from .base_controller import BaseController
from managers import MeManager
from fastapi import Response, status, Depends
from fastapi_cloudauth.cognito import Cognito
from fastapi.responses import JSONResponse
from utilities.auth import get_current_user
from fastapi_cloudauth.cognito import CognitoClaims
from pydantic import BaseModel, Field

class PostItem(BaseModel):
    vendor_type: str = Field(alias="vendorType")

class MeController(BaseController):

    def __init__(self, auth: Cognito):
        super().__init__(auth)
        self.router.add_api_route("/me", self.get, methods=["GET"])
        self.router.add_api_route("/me", self.patch, methods=["PATCH"])
        self.router.add_api_route("/me", self.post, methods=["POST"])

    async def get(self, current_user: CognitoClaims = Depends(get_current_user)) -> JSONResponse:
        result = await MeManager().get_user(current_user)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=result
        )

    async def patch(self, current_user: CognitoClaims = Depends(get_current_user)) -> JSONResponse:
        # TODO
        return JSONResponse(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            content="Not implemented yet" 
        )

    async def post(self, item: PostItem, current_user: CognitoClaims = Depends(get_current_user)) -> Response:
        ret = await MeManager().create_user(current_user.sub, item.vendor_type)
        if not ret:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"error": "Failed to make user"}
            ) 
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"contractId": ret}
        )
