from docusign_esign import ApiClient, OAuthToken
from typing import List

def get_jwt_token(private_key: str, scopes: List[str], auth_server: str, client_id: str, impersonated_user_id: str) -> OAuthToken:
    """Get the jwt token"""
    api_client = ApiClient()
    api_client.set_base_path(auth_server)
    response = api_client.request_jwt_user_token(
        client_id=client_id,
        user_id=impersonated_user_id,
        oauth_host_name=auth_server,
        private_key_bytes=private_key,
        expires_in=4000,
        scopes=scopes
    )
    return response

def create_api_client(base_path: str, access_token: str) -> ApiClient:
    """Create api client and construct API headers"""
    api_client = ApiClient()
    api_client.host = base_path
    api_client.set_default_header(header_name="Authorization", header_value=f"Bearer {access_token}")

    return api_client

