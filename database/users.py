from typing import Optional
from utilities.types import JSONDict, MongoMappingType
import pymongo
from utilities.rbac import Roles, Groups
import pymongo.results
from .base_db import BaseDB
from motor.motor_asyncio import AsyncIOMotorCollection


class UsersDB(BaseDB):

    @classmethod
    def _new_user(cls, _id: str, username: str, vendor_type: str) -> JSONDict:
        return {
            "_id": _id,
            "username": username,
            "contracts": [],
            "group": Groups.CUSTOMER,
            "vendor_type": vendor_type,
            "roles": []
        }

    @classmethod
    async def get_user(cls, uuid: str) -> Optional[MongoMappingType]:
        query = {"_id": uuid}
        result: Optional[MongoMappingType] = await cls.get_collection().find_one(query)
        return result

    @classmethod
    async def create_user(cls, uuid: str, username: str, vendor_type: str) -> bool:
        query = cls._new_user(uuid, username, vendor_type)
        # TODO catch error if user already exists
        ret: pymongo.results.InsertOneResult = await cls.get_collection().insert_one(query)
        return ret.acknowledged

    @classmethod
    def get_collection(cls) -> AsyncIOMotorCollection:  # type: ignore[no-any-unimported]
        return super().get_database()['users']

    @classmethod
    async def add_user_contract(cls, uuid: str, contract_id: str) -> pymongo.results.UpdateResult:
        result: pymongo.results.UpdateResult = await cls.get_collection().update_one(
            {"_id": uuid},
            {"$addToSet": {"contracts": contract_id}}
        )
        return result

    # TODO this needs to be reworked
    @classmethod
    async def _get_random_reviewer(cls, role: str) -> Optional[MongoMappingType]:
        query = {
            "$and": [
                {
                    "roles": {
                        "$in": [role]
                    }
                },
                {
                    "group": {
                        "$in": [Groups.DEVELOPER, Groups.STAFF]
                    }
                }
            ]
        }
        results = await cls.get_random(cls.get_collection(), 1, query)
        if len(results) == 0:
            return None
        assert len(results) == 1, "Recieved too many results"
        return results[0]

    @classmethod
    async def get_random_artist_reviewer(cls) -> Optional[MongoMappingType]:
        return await cls._get_random_reviewer(Roles.ARTIST_REVIEWER)

    @classmethod
    async def get_random_dealer_reviewer(cls) -> Optional[MongoMappingType]:
        return await cls._get_random_reviewer(Roles.DEALER_REVIEWER)
