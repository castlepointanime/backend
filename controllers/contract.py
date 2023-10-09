from managers import ContractManager
from .base_controller import BaseController
from utilities import NoApproverException
from utilities.types import HelperModel
from typing import Optional
from fastapi_cloudauth.cognito import Cognito
from fastapi_cloudauth.cognito import CognitoClaims
from utilities.auth import get_current_user
from fastapi import status, Depends, Response, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from utilities.types.fields import phone_number
from config import Config
from typing import List
from database.users import UsersDB

config = Config()


class PostItem(BaseModel):
    artist_phone_number: int = phone_number("artistPhoneNumber")
    helpers: Optional[List[HelperModel]] = Field(alias="helpers", min_length=1, max_length=config.get_contract_limit("max_helpers"))
    num_additional_chairs: int = Field(alias="numAdditionalChairs", le=config.get_contract_limit("max_additional_chairs"), ge=0, examples=['2'])


class PostResponseItem(BaseModel):
    contractId: int = 0


class ContractController(BaseController):

    def __init__(self, auth: Cognito):  # type: ignore[no-any-unimported]
        super().__init__(auth)
        self.router.add_api_route("/contract", self.post, methods=["POST"], response_model=PostResponseItem)

    async def post(self, item: PostItem, current_user: CognitoClaims = Depends(get_current_user)) -> Response:  # type: ignore[no-any-unimported]
        db = await UsersDB.get_user(current_user.sub)
        if not db:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='User needs to make an account'
            )

        try:
            result = await ContractManager().create_contract(
                current_user.sub,
                contract_type=str(db.get("vendor_type")),
                helpers=item.helpers,
                num_additional_chairs=item.num_additional_chairs,
                signer_email=current_user.email,  # TODO assert that emails are verified
                signer_name=current_user.username,
                artist_phone_number=item.artist_phone_number  # TODO this should be stored in AWS
                )
        except NoApproverException:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Cannot make contract since there is nobody to approve the contract'
            )

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=result
        )
