import sys, os
from .envelope import Contract
from docusign import ContractData
from docusign_esign import ApiClient
from docusign_esign.client.api_exception import ApiException
from .jwt_config import get_jwt_token
from .ds_config import DS_JWT
from .env import DOCUSIGN_PRIVATE_KEY
import logging

SCOPES = [
    "signature", "impersonation"
]

class Docusign:
    
    @classmethod
    def _get_consent_url(cls):
        url_scopes = "+".join(SCOPES)

        # Construct consent URL
        redirect_uri = "https://developers.docusign.com/platform/auth/consent"
        consent_url = f"https://{DS_JWT['authorization_server']}/oauth/auth?response_type=code&" \
                    f"scope={url_scopes}&client_id={DS_JWT['ds_client_id']}&redirect_uri={redirect_uri}"

        return consent_url

    @classmethod
    def _get_token(cls, private_key, api_client):
        # Call request_jwt_user_token method
        token_response = get_jwt_token(private_key, SCOPES, DS_JWT["authorization_server"], DS_JWT["ds_client_id"],
                                    DS_JWT["ds_impersonated_user_id"])
        access_token = token_response.access_token

        # Save API account ID
        user_info = api_client.get_user_info(access_token)
        accounts = user_info.get_accounts()
        api_account_id = accounts[0].account_id
        base_path = accounts[0].base_uri + "/restapi"
        return {"access_token": access_token, "api_account_id": api_account_id, "base_path": base_path}

    @classmethod
    def _handle_consent(cls, err, callback, api_client, private_key: str, contract_data: ContractData):
        body = err.body.decode('utf8')

        if "consent_required" in body:
            consent_url = cls._get_consent_url()
            logging.warn("Open the following URL in your browser to grant consent to the application:")
            logging.warn(consent_url)
            consent_granted = input("Consent granted? Select one of the following: \n 1)Yes \n 2)No \n")
            if consent_granted == "1":
                return callback(api_client, private_key, contract_data)
            else:
                sys.exit("Please grant consent")
        else:
            logging.info(body)
            
    @classmethod
    def _run(cls, api_client, private_key: str, contract_data: ContractData):
        jwt_values = cls._get_token(private_key, api_client)
        
        access_token=jwt_values["access_token"]
        base_path=jwt_values["base_path"]
        account_id=jwt_values["api_account_id"]
        
        envelope_id = Contract(access_token, base_path, account_id).make_contract(contract_data)
        
        logging.info("Your envelope has been sent.")
        return envelope_id
    
    @classmethod
    def _auth(cls):
        api_client = ApiClient()
        api_client.set_base_path(DS_JWT["authorization_server"])
        api_client.set_oauth_host_name(DS_JWT["authorization_server"])

        private_key = DOCUSIGN_PRIVATE_KEY.encode("ascii").decode("utf-8")
        
        return [api_client, private_key]
    
    @classmethod
    def create_contract(cls, contract_data: ContractData):
        api_client, private_key = cls._auth()
        try:
            return cls._run(api_client, private_key, contract_data)
        except ApiException as err:
            return cls._handle_consent(err, cls._run, api_client, private_key, contract_data)
        