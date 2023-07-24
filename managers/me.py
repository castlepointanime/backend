
from utilities import FlaskResponses
from utilities.types import FlaskResponseType


class MeManager():

    def get_user(self, current_user, current_cognito_jwt) -> FlaskResponseType:
        return FlaskResponses().success({
            'name': str(current_user),
            'email': str(current_cognito_jwt['email']),
            'database': current_cognito_jwt['database']
        })
