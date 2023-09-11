from motor.motor_asyncio import AsyncIOMotorCollection
from .base_db import BaseDB
from typing import Optional
from utilities.types import JSONDict, MongoMappingType
import pymongo
from utilities.rbac import Roles, Groups
import pymongo.results


class UsersDB(BaseDB):

    @classmethod
    def _new_user(cls, _id: str, vendor_type: str) -> JSONDict:
        return {
            "_id": _id,
            "contracts": [],
            "group": Groups.CUSTOMER,
            "vendor_type": vendor_type,
            "roles": []
        }

    @classmethod
    def get_user(cls, uuid: str) -> Optional[MongoMappingType]:
        query = {"_id": uuid}
        return cls.get_collection().find_one(query)

    @classmethod
    async def create_user(cls, uuid: str, vendor_type: str) -> bool:
        query = cls._new_user(uuid, vendor_type)
        # TODO catch error if user already exists
        ret: pymongo.results.InsertOneResult = await cls.get_collection_async().insert_one(query)
        return ret.acknowledged

    @classmethod
    def get_collection(cls) -> pymongo.collection.Collection[MongoMappingType]:
        return super().get_database()['users']

    @classmethod
    def get_collection_async(cls) -> AsyncIOMotorCollection:  # type: ignore[no-any-unimported]
        return super().get_database_async()['users']

    @classmethod
    async def add_user_contract(cls, uuid: str, contract_id: str) -> pymongo.results.UpdateResult:
        return await cls.get_collection_async().update_one(
            {"_id": uuid},
            {"$addToSet": {"contracts": contract_id}}
        )

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
        results = cls.get_random(await cls.get_collection_async(), 1, query)
        if len(results) == 0:
            return None
        assert len(results) == 1
        return results[0]

    @classmethod
    async def get_random_artist_reviewer(cls) -> Optional[MongoMappingType]:
        return await cls._get_random_reviewer(Roles.ARTIST_REVIEWER)

    @classmethod
    async def get_random_dealer_reviewer(cls) -> Optional[MongoMappingType]:
        return await cls._get_random_reviewer(Roles.DEALER_REVIEWER)
