from managers import ContractManager
from flasgger import swag_from
from .base_controller import BaseController
from utilities.types import FlaskResponseType
from utilities import FlaskResponses
from .swagger.contract.post import contract_post_schema


class ContractController(BaseController):

    @swag_from(contract_post_schema)
    def post(self) -> FlaskResponseType:
        data = self.get_request_data(contract_post_schema, "ContractData")

        try:
            result = ContractManager().create_contract(
                contract_type=data['contractType'],
                helpers=data.get('helpers'),
                num_additional_chairs=data['numAdditionalChairs'],
                signer_email=data['signerEmail'],
                signer_name=data['signerName'],
                artist_phone_number=data['artistPhoneNumber']
                )
        except NotImplementedError:
            return FlaskResponses.not_implemented_yet()

        return FlaskResponses.success(result)
