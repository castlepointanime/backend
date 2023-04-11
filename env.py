import os
from dotenv import load_dotenv
load_dotenv('../backend.env')

COGNITO_REGION=os.getenv("COGNITO_REGION")
COGNITO_USERPOOL_ID=os.getenv("COGNITO_USERPOOL_ID")
COGNITO_APP_CLIENT_ID=os.getenv("COGNITO_APP_CLIENT_ID")