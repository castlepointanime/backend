import os
from dotenv import load_dotenv
load_dotenv('../../../../backend.env')

DOCUSIGN_CLIENT_ID=os.getenv("DOCUSIGN_CLIENT_ID")
DOCUSIGN_IMPERSONATED_USER_ID=os.getenv("DOCUSIGN_IMPERSONATED_USER_ID")
DOCUSIGN_PRIVATE_KEY=os.getenv("DOCUSIGN_PRIVATE_KEY")
CONTRACT_TEMPLATE_ID=os.getenv("CONTRACT_TEMPLATE_ID")