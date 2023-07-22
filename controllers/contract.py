from managers import ContractManager
from flasgger import swag_from
from flask import request, Response
from .base_controller import BaseController
from utilities.types import FlaskResponseType

class ContractController(BaseController):

    SWAGGER_POST_PATH = "swagger/contract/post.yaml"

    @swag_from(SWAGGER_POST_PATH)
    def post(self) -> FlaskResponseType:
        data = self.get_request_data(self.SWAGGER_POST_PATH, "ContractData")
        return ContractManager().create_contract(
            contract_type=data['contractType'],
            helpers=data.get('helpers'),
            num_additional_chairs=data['numAdditionalChairs'],
            signer_email=data['signerEmail'],
            signer_name=data['signerName'],
            artist_phone_number=data['artistPhoneNumber']
            )