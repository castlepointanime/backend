import logging
import re
from docusign import Docusign, ContractData
from base_request import BaseRequest
from helpers import FLASK_ERROR_TYPE
from typing import Optional, List, Dict
import datetime

REQUIRED_KEYS = ['contractType', 'helperBadgeQt', 'additionalChairsQt', 'artistNumber', \
    'signerName', 'email']

OPTIONAL_KEYS = ['helpers']

MAX_HELPERS = 3

class CreateContractRequest(BaseRequest):
    """
    TODO add docstring of the API route, explaining each key and an example API call
    """

    def __init__(self):
        self._helpers : List[Dict] = [{}] * MAX_HELPERS

    def _verify_valid_request(self) -> Optional[FLASK_ERROR_TYPE]:
        # Returns data if there was an error. If request is valid, returns None

        # check if content contains all required keys
        for key in REQUIRED_KEYS:
            if key not in self.content.keys():
                return self.errors.missing_or_invalid_field(key)

        if not self.validation.is_valid_contract_type(self.content['contractType']):
            return self.errors.missing_or_invalid_field('contractType')
        
        #TODO need to discuss spec for dealer contract
        if self.content['contractType'] == "dealer":
            return self.errors.not_implemented_yet()

        if not self.validation.is_valid_helper_badge_quantity(self.content['helperBadgeQt']):
            return self.errors.missing_or_invalid_field('helperBadgeQt')

        if not self.validation.is_valid_additional_chairs_quantity(self.content['additionalChairsQt']):
            return self.errors.missing_or_invalid_field('additionalChairsQt')

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
        
        if self.content.get('helpers'):
            self._helpers = [{}] * MAX_HELPERS
            for helper in self.content['helpers']:

                # Error check
                helper_number = helper.get('number')
                if(not self.validation.is_valid_phone_number(helper_number)):
                    self._helpers = [{}] * MAX_HELPERS
                    return self.errors.missing_or_invalid_field('helper number')
                
                helper_name = helper.get('name')
                if(type(helper_name) != str):
                    self._helpers = [{}] * MAX_HELPERS
                    return self.errors.missing_or_invalid_field('helper name')

                self._helpers.append({'number': helper_number, 'name': helper_name})

        return None # validation was successful. No error will be returned

    def create_contract(self, request):

        if not self.generate_request_content(request):
            return self.errors.request_not_json_error()
    
        error = self._verify_valid_request()
        if error:
            logging.warn(error)
            return error

        current_date = datetime.datetime.now()
        day = int(current_date.strftime('%d'))
        month = current_date.strftime('%B')
        shortened_year = int(current_date.strftime('%Y')[2:])

        # TODO randomly select admin from DB and assign as approver.
        approver_email = "TEST@gmail.com"
        approver_name = "test"
        
        try:
            data = ContractData(
                month=month,
                signer_email=self.content['email'],
                helper_badge_qt=self.content['helperBadgeQt'],
                additional_chairs_qt=self.content['additionalChairsQt'],
                artist_number=self.content['artistNumber'],
                helper1_name=self._helpers[0].get('name'),
                helper1_number=self._helpers[0].get('number'),
                helper2_name=self._helpers[1].get('name'),
                helper2_number=self._helpers[1].get('number'),
                helper3_name=self._helpers[2].get('name'),
                helper3_number=self._helpers[2].get('number'),
                shortened_year=shortened_year,
                day=day,
                signer_name=self.content['signerName'],
                approver_name=approver_name,
                approver_email=approver_email,
            )

            docusign = Docusign()
            
            return {'contractId': docusign.create_contract(data)}, 200
        except Exception as e:
            logging.warn(e)
            return {'error': "Oopsie woopsie, the docusign function broke :3"}, 500
        
