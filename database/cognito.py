# https://docs.aws.amazon.com/code-library/latest/ug/python_3_cognito-identity-provider_code_examples.html

from botocore.exceptions import ClientError
import logging
import boto3
from config.env import COGNITO_USERPOOL_ID, COGNITO_REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN

class CognitoIdentityProviderWrapper:
    """Encapsulates Amazon Cognito actions"""
    def __init__(self):
        self.cognito_idp_client = boto3.client('cognito-idp',
                                               region_name=COGNITO_REGION,
                                               aws_access_key_id=AWS_ACCESS_KEY_ID,
                                               aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                                               aws_session_token=AWS_SESSION_TOKEN
                                               )
    
    def get_user(self, username: str):
        """
        Gets a user in Cognito by it's username.

        :return: user
        """
        try:
            response = self.cognito_idp_client.admin_get_user(UserPoolId=COGNITO_USERPOOL_ID, Username=username)
            user = response
        except ClientError as err:
            logging.error(
                "Couldn't list users for %s. Here's why: %s: %s", COGNITO_USERPOOL_ID,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
        else:
            return user