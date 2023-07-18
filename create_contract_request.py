import logging
import re
from Docusign import Docusign
from ContractData import ContractData
from base_request import BaseRequest
from helpers import FLASK_ERROR_TYPE

REQUIRED_KEYS = ['contractType', 'month', 'helperBadgeQt', 'additionalChairsQt', 'artistNumber', \
    'shortenedYear', 'day', 'signerName', 'approverName', 'approverEmail']

class CreateContractRequest(BaseRequest):
    """
    TODO add docstring of the API route, explaining each key and an example API call
    """

    def _verify_valid_request(self) -> Optional[None, FLASK_ERROR_TYPE]:
        # Returns data if there was an error. If request is valid, returns None

        # check if content contains all required keys
        for key in REQUIRED_KEYS:
            if key not in self.content.keys():
                return self.errors.missing_key_field(key)

        if not self.validation.is_valid_contract_type(self.content['contractType']):
            return self.errors.missing_or_invalid_field('contractType')
        
        #TODO need to discuss spec for dealer contract
        if self.content['contractType'] == "dealer":
            return self.errors.not_implemented_yet()

        if not self.validation.is_valid_month_name(self.content['month']):
            return self.errors.missing_or_invalid_field('month')
        
        if not self.validation.is_valid_helper_badge_quantity(self.content['helperBadgeQt']):
            return self.errors.missing_or_invalid_field('helperBadgeQt')

        if not self.validation.is_valid_additional_chairs_quantity(self.content['additionalChairsQt']):
            return self.errors.missing_or_invalid_field('additionalChairsQt')

        year = self.content['shortenedYear']
        day = self.content['day']
        month = self.content['month']
        if (not self.validation.is_valid_date(year, month, day)):
            return self.errors.invalid_date()

        if type(self.content['signerName']) != str:
            return self.errors.missing_or_invalid_field('signerName')
        
        if not self.validation.is_valid_email(self.content['email']):
            return self.errors.missing_or_invalid_field('email')

        if type(self.content['approverName']) != str:
            return self.errors.missing_or_invalid_field('approverName')
        
        if not self.validation.is_valid_email(self.content['approverEmail']):
            return self.errors.missing_or_invalid_field('approverEmail')

        if not self.validation.is_valid_phone_number(self.content['artistNumber']):
            return self.errors.missing_or_invalid_field('artistNumber')
        
        for i in range(self.content['helperBadgeQt']):

            # Generate keys dynamically
            helper_key= f"helper{i+1}Number"
            helper_name_key = f"{helper_key}Number"
            helper_number_key = f"{helper_key}Name"

            # Error check
            if(not self.validation.is_valid_phone_number(self.content.get(helper_number_key))):
                return self.errors.missing_or_invalid_field(helper_number_key)
            if(type(self.content.get(helper_name_key)) != str):
                return self.errors.missing_or_invalid_field(helper_name_key)

        return None # validation was successful. No error will be returned

    def create_contract(self, request):

        if not self.generate_request_content():
            return self.errors.request_not_json_error()
    
        error = self._verify_valid_request()
        if error:
            logging.warn(error)
            return error
        
        try:
            data = ContractData(
                month=self.content['month'],
                email=self.content['email'],
                helper_badge_qt=self.content['helperBadgeQt'],
                additional_chairs_qt=self.content['additionalChairsQt'],
                helper1_name=self.content.get('helper1Name'),
                helper1_number=self.content.get('helper1Number'),
                helper2_name=self.content.get('helper2Name'),
                helper2_number=self.content.get('helper2Number'),
                helper3_name=self.content.get('helper3Name'),
                helper3_number=self.content.get('helper3Number'),
                shortened_year=self.content['shortenedYear'],
                day=self.content['day'],
                signer_name=self.content['signerName'],
                aprover_name=self.content['approverName'],
                aprover_email=self.content['approverEmail']
            )
            
            return {'contractId': data.generate_envelope()}, 200
        except Exception as e:
            logging.warn(e)
            return {'error': "Oopsie woopsie, the docusign function broke :3"}, 500
        
