# ds_config.py
#
# DocuSign configuration settings
from .env import DOCUSIGN_CLIENT_ID, DOCUSIGN_IMPERSONATED_USER_ID

DS_JWT = {
    "ds_client_id": DOCUSIGN_CLIENT_ID,
    # The id of the user.
    "ds_impersonated_user_id": DOCUSIGN_IMPERSONATED_USER_ID,
    "authorization_server": "account-d.docusign.com"
}
