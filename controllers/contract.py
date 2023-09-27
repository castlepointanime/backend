from managers import ContractManager
from .base_controller import BaseController
from utilities import NoApproverException
from utilities.types import JSONDict, HelperData
from typing import Optional
from fastapi_cloudauth.cognito import Cognito
from fastapi_cloudauth.cognito import CognitoClaims
from utilities.auth import get_current_user
from fastapi import status, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional

class PostItem(BaseModel):
    artist_phone_number: int = Field(alias="artistPhoneNumber")
    helpers: Optional[HelperData] = None 
    num_additional_chairs: int = Field(alias="numAdditionalChairs")

class ContractController(BaseController):

    def __init__(self, auth: Cognito):
        super().__init__(auth)
        self.router.add_api_route("/contract", self.post, methods=["POST"])

    async def post(self, item: PostItem, current_user: CognitoClaims = Depends(get_current_user)) -> JSONResponse:
        user_db: Optional[JSONDict] = current_user.database
        if user_db is None:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST, 
                content={'error': 'User needs to make an account'}
            )

        try:
            result = await ContractManager().create_contract(
                current_user.sub,
                contract_type=user_db['vendor_type'],
                helpers=item.helpers,
                num_additional_chairs=item.num_additional_chairs,
                signer_email=current_user.email,  # TODO assert that emails are verified
                signer_name=current_user.username,
                artist_phone_number=item.artist_phone_number  # TODO this should be stored in AWS
                )
        except NoApproverException:
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content={'error': 'Cannot make contract since there is nobody to approve the contract'}
            )

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=result
        )
