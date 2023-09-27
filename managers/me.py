from werkzeug.local import LocalProxy
from utilities.types import JSONDict
from typing import Dict, Optional
from database import UsersDB
from utilities.types import MongoMappingType
from fastapi_cloudauth.cognito import CognitoClaims

class MeManager():

    async def get_user_from_db(cls, user_id: str) -> Optional[MongoMappingType]:
        return await UsersDB().get_user(user_id)

    async def get_user(self, current_user: CognitoClaims) -> Dict[str, str]:
        
        return {
            'name': str(current_user.username),
            'email': str(current_user.email),
            'database': await self.get_user_from_db(current_user.sub)
        }

    async def create_user(self, user_id: str, vendor_type: str) -> bool:
        return await UsersDB.create_user(user_id, vendor_type)
