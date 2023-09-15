from werkzeug.local import LocalProxy
from utilities.types import JSONDict
from typing import Dict, Optional
from database import UsersDB
from utilities.types import MongoMappingType


class MeManager():

    def get_user_from_db(cls, user_id: str) -> Optional[MongoMappingType]:
        return UsersDB().get_user(user_id)

    def get_user(self, current_user: str, current_cognito_jwt: LocalProxy[JSONDict]) -> Dict[str, str]:
        return {
            'name': str(current_user),
            'email': str(current_cognito_jwt['email']),
            'database': current_cognito_jwt['database']
        }

    def create_user(self, user_id: str, username: str, vendor_type: str) -> bool:
        return UsersDB.create_user(user_id, username, vendor_type)
