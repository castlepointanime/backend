from flask_cognito import cognito_auth_required, current_cognito_jwt, current_user
from managers import ContractManager
from flasgger import swag_from
from .base_controller import BaseController
from utilities.types import FlaskResponseType
from utilities import FlaskResponses, NoApproverException
from .swagger.contract.post import contract_post_schema
from utilities.types import JSONDict
from typing import Optional


class ContractController(BaseController):

    @cognito_auth_required
    @swag_from(contract_post_schema)
    def post(self) -> FlaskResponseType:
        data = self.get_request_data(contract_post_schema, "ContractData")

        user_db: Optional[JSONDict] = current_cognito_jwt['database']
        if user_db is None:
            return FlaskResponses.bad_request("User needs to make an account")

        try:
            result = ContractManager().create_contract(
                current_cognito_jwt['sub'],
                contract_type=user_db['vendor_type'],
                helpers=data.get('helpers'),
                num_additional_chairs=data['numAdditionalChairs'],
                signer_email=current_cognito_jwt['email'],  # TODO assert that emails are verified
                signer_name=str(current_user),
                artist_phone_number=data['artistPhoneNumber']
                )
        except NoApproverException:
            return FlaskResponses.conflict("Cannot make contract since there is nobody to approve the contract.")

        return FlaskResponses.success(result)
