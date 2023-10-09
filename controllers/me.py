from .base_controller import BaseController
from managers import MeManager
from fastapi import Response, status, Depends, HTTPException
from fastapi_cloudauth.cognito import Cognito
from fastapi.responses import JSONResponse
from utilities.auth import get_current_user
from fastapi_cloudauth.cognito import CognitoClaims
from pydantic import BaseModel, Field, EmailStr, UUID4
from utilities.types.fields import VendorTypeEnum
from typing import List
from typing_extensions import TypedDict
import uuid
from database.users import UsersDB


class PostItem(BaseModel):
    vendor_type: VendorTypeEnum = Field(alias="vendorType")


class PostResponseItem(BaseModel):
    created: bool = True


class GetDatabaseModel(TypedDict, total=True):
    _id: UUID4
    Group: str
    Roles: List[str]
    contracts: List[UUID4]
    vendorType: VendorTypeEnum


class GetResponseItem(BaseModel):
    email: EmailStr = "bob123@mail.com"
    name: str = "Bob"
    database: GetDatabaseModel = GetDatabaseModel(
        Group="Customer",
        _id=uuid.uuid4(),
        Roles=["CanEditCustomer"],
        contracts=[
            uuid.uuid4(),
        ],
        vendorType=VendorTypeEnum.artist
        )


class MeController(BaseController):

    def __init__(self, auth: Cognito):  # type: ignore[no-any-unimported]
        super().__init__(auth)
        self.router.add_api_route("/me", self.get, methods=["GET"], response_model=GetResponseItem)
        self.router.add_api_route("/me", self.patch, methods=["PATCH"])
        self.router.add_api_route("/me", self.post, methods=["POST"], response_model=PostResponseItem)

    async def get(self, current_user: CognitoClaims = Depends(get_current_user)) -> Response:  # type: ignore[no-any-unimported]
        result = await UsersDB.get_user(current_user.sub)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "name": current_user.username,
                "email": current_user.email,
                "database": result
            }
        )

    async def patch(self, current_user: CognitoClaims = Depends(get_current_user)) -> Response:  # type: ignore[no-any-unimported]
        # TODO
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Not implemented yet"
        )

    async def post(self, item: PostItem, current_user: CognitoClaims = Depends(get_current_user)) -> Response:  # type: ignore[no-any-unimported]
        ret: bool = await MeManager().create_user(current_user.sub, str(item.vendor_type))
        if not ret:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to make user"
            )
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"created": ret}
        )
