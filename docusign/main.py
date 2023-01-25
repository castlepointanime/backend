import sys, os
from envelope import Contract

from docusign_esign import ApiClient
from docusign_esign.client.api_exception import ApiException
from jwt_config import get_jwt_token
from ds_config import DS_JWT
from env import DOCUSIGN_PRIVATE_KEY

SCOPES = [
    "signature", "impersonation"
]


def get_consent_url():
    url_scopes = "+".join(SCOPES)

    # Construct consent URL
    redirect_uri = "https://developers.docusign.com/platform/auth/consent"
    consent_url = f"https://{DS_JWT['authorization_server']}/oauth/auth?response_type=code&" \
                  f"scope={url_scopes}&client_id={DS_JWT['ds_client_id']}&redirect_uri={redirect_uri}"

    return consent_url


def get_token(private_key, api_client):
    # Call request_jwt_user_token method
    token_response = get_jwt_token(private_key, SCOPES, DS_JWT["authorization_server"], DS_JWT["ds_client_id"],
                                   DS_JWT["ds_impersonated_user_id"])
    access_token = token_response.access_token

    # Save API account ID
    user_info = api_client.get_user_info(access_token)
    accounts = user_info.get_accounts()
    api_account_id = accounts[0].account_id
    print(api_account_id)
    base_path = accounts[0].base_uri + "/restapi"

    print(base_path)
    return {"access_token": access_token, "api_account_id": api_account_id, "base_path": base_path}


def run_example(private_key, api_client):
    jwt_values = get_token(private_key, api_client)
    envelope_id = Contract.worker(
        jwt_values["access_token"], jwt_values["base_path"], jwt_values["api_account_id"])
    print("Your envelope has been sent.")
    print(envelope_id)


def main():
    api_client = ApiClient()
    api_client.set_base_path(DS_JWT["authorization_server"])
    api_client.set_oauth_host_name(DS_JWT["authorization_server"])

    private_key = DOCUSIGN_PRIVATE_KEY.encode("ascii").decode("utf-8")

    try:
        run_example(private_key, api_client)
    except ApiException as err:
        body = err.body.decode('utf8')

        if "consent_required" in body:
            consent_url = get_consent_url()
            print(
                "Open the following URL in your browser to grant consent to the application:")
            print(consent_url)
            consent_granted = input(
                "Consent granted? Select one of the following: \n 1)Yes \n 2)No \n")
            if consent_granted == "1":
                run_example(private_key, api_client)
            else:
                sys.exit("Please grant consent")
        else:
            print(body)


main()
