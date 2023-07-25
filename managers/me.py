from werkzeug.local import LocalProxy
from utilities.types import JSONDict
from typing import Dict


class MeManager():

    def get_user(self, current_user: str, current_cognito_jwt: LocalProxy[JSONDict]) -> Dict[str, str]:
        return {
            'name': str(current_user),
            'email': str(current_cognito_jwt['email']),
            'vendor_type': current_cognito_jwt['custom:vendor_type'],
            'database': current_cognito_jwt['database']
        }
