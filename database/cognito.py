# https://docs.aws.amazon.com/code-library/latest/ug/python_3_cognito-identity-provider_code_examples.html

from botocore.exceptions import ClientError
import logging
import boto3
from config.env import COGNITO_USERPOOL_ID, COGNITO_REGION

class CognitoIdentityProviderWrapper:
    """Encapsulates Amazon Cognito actions"""
    def __init__(self):
        self.cognito_idp_client = boto3.client('cognito-idp')
    
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