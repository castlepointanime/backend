from fastapi_cloudauth.cognito import CognitoCurrentUser, CognitoClaims
from config.env import COGNITO_APP_CLIENT_ID, COGNITO_REGION, COGNITO_USERPOOL_ID
from pydantic import Field

class CustomAuthClaims(CognitoClaims):
    sub: str = Field(alias="sub")

get_current_user = CognitoCurrentUser(
    region=COGNITO_REGION, 
    userPoolId=COGNITO_USERPOOL_ID,
    client_id=COGNITO_APP_CLIENT_ID
).claim(CustomAuthClaims)