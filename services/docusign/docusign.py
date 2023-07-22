import sys, os
from .envelope import Contract
from services.docusign import ContractData
from docusign_esign import ApiClient
from docusign_esign.client.api_exception import ApiException
from .jwt_config import get_jwt_token
from .ds_config import DS_JWT
from .env import DOCUSIGN_PRIVATE_KEY
import logging
from typing import Dict, Callable, List, Optional

SCOPES = [
    "signature", "impersonation"
]

class Docusign:
    
    @classmethod
    def _get_consent_url(cls) -> str:
        url_scopes = "+".join(SCOPES)

        # Construct consent URL
        redirect_uri = "https://developers.docusign.com/platform/auth/consent"
        consent_url = f"https://{DS_JWT['authorization_server']}/oauth/auth?response_type=code&" \
                    f"scope={url_scopes}&client_id={DS_JWT['ds_client_id']}&redirect_uri={redirect_uri}"

        return consent_url

    @classmethod
    def _get_token(cls, private_key: str, api_client: ApiClient) -> Dict[str, str]:
        # Call request_jwt_user_token method
        
        authorization_server = DS_JWT.get("authorization_server")
        if type(authorization_server) != str:
            raise ValueError("Authorization server is not in DS Config")

            
        ds_client_id = DS_JWT.get("ds_client_id")
        if (type(ds_client_id) != str):
            raise ValueError("DS Client ID is not in environment")

        ds_impersonated_user_id = DS_JWT.get("ds_impersonated_user_id")
        if (type(ds_impersonated_user_id) != str):
            raise ValueError("DS Impersonated User ID is not in environment")

        token_response = get_jwt_token(private_key, SCOPES, authorization_server, ds_client_id,
                                    ds_impersonated_user_id)
        access_token = token_response.access_token

        # Save API account ID
        user_info = api_client.get_user_info(access_token)
        accounts = user_info.get_accounts()
        api_account_id = accounts[0].account_id
        base_path = accounts[0].base_uri + "/restapi"
        return {"access_token": access_token, "api_account_id": api_account_id, "base_path": base_path}

    @classmethod
    def _handle_consent(cls, err: ApiException, callback: Callable[[ApiClient, str, ContractData], str], api_client: ApiClient, private_key: str, contract_data: ContractData) -> str:
        body = err.body.decode('utf8')

        if "consent_required" in body:
            consent_url = cls._get_consent_url()
            logging.warn("Open the following URL in your browser to grant consent to the application:")
            logging.warn(consent_url)
            consent_granted = input("Consent granted? Select one of the following: \n 1)Yes \n 2)No \n")
            if consent_granted == "1":
                return callback(api_client, private_key, contract_data)
        
        logging.error(body)
        sys.exit("Failed to grant consent") #TODO can this sys.exit be removed?   
            
    @classmethod
    def _run(cls, api_client: ApiClient, private_key: str, contract_data: ContractData) -> str:
        jwt_values = cls._get_token(private_key, api_client)
        
        access_token=jwt_values["access_token"]
        base_path=jwt_values["base_path"]
        account_id=jwt_values["api_account_id"]
        
        envelope_data : Dict[str, str] = Contract(access_token, base_path, account_id).make_contract(contract_data)
        
        if type(envelope_data) is not dict:
            raise ValueError(f"Invalid envelope response: {envelope_data}")

        if "envelope_id" not in envelope_data:
            raise ValueError(f"Envelope does not contain ID: {envelope_data}")

        envelope_id : Optional[str] = envelope_data["envelope_id"]
        if type(envelope_id) != str:
            raise ValueError(f"Invalid envelope id {envelope_id} of type {type(envelope_id)}")
        
        logging.info("Your envelope has been sent.")
        return envelope_id
    
    @classmethod
    def _auth(cls) -> List[str]:
        api_client = ApiClient()
        api_client.set_base_path(DS_JWT["authorization_server"])
        api_client.set_oauth_host_name(DS_JWT["authorization_server"])

        if DOCUSIGN_PRIVATE_KEY is None:
            raise ValueError("No private key in environment")

        private_key = DOCUSIGN_PRIVATE_KEY.encode("ascii").decode("utf-8")
        
        return [api_client, private_key]
    
    @classmethod
    def create_contract(cls, contract_data: ContractData) -> str:
        api_client, private_key = cls._auth()
        try:
            return cls._run(api_client, private_key, contract_data)
        except ApiException as err:          
            return cls._handle_consent(err, cls._run, api_client, private_key, contract_data)
        