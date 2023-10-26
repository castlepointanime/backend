# https://docs.aws.amazon.com/code-library/latest/ug/python_3_cognito-identity-provider_code_examples.html

from botocore.exceptions import ClientError
import logging
import boto3
from config.env import COGNITO_USERPOOL_ID
from utilities.types import JSONDict
from distutils.util import strtobool


class CognitoUser:

    def __init__(self, cognito_response_json: JSONDict) -> None:
        assert cognito_response_json.get("UserAttributes")
        for attribute_dict in cognito_response_json['UserAttributes']:
            assert "Name" in attribute_dict
            assert attribute_dict.get("Value")
            match attribute_dict['Name']:
                case 'sub':
                    self.sub: str = attribute_dict['Value']
                case 'email_verified':
                    self.email_verified: bool = bool(strtobool(attribute_dict['Value']))
                case 'email':
                    self.email: str = attribute_dict['Value']
        assert self.sub is not None
        assert self.email_verified is not None
        assert self.email is not None


class CognitoIdentityProviderWrapper:
    """Encapsulates Amazon Cognito actions"""
    def __init__(self) -> None:
        self.cognito_idp_client = boto3.client('cognito-idp')

    def get_user(self, username: str) -> CognitoUser:
        """
        Gets a user in Cognito by it's username.

        :return: user
        """
        try:
            response: JSONDict = self.cognito_idp_client.admin_get_user(UserPoolId=COGNITO_USERPOOL_ID, Username=username)
            assert type(response) is dict
            return CognitoUser(response)
        except ClientError as err:
            logging.error(
                "Couldn't list users for %s. Here's why: %s: %s", COGNITO_USERPOOL_ID,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise err
