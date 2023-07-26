from motor.motor_asyncio import AsyncIOMotorCollection
from .base_db import BaseDB
from typing import Optional
from utilities.types import JSONDict, MongoMappingType
from typing import Collection


class UsersDB(BaseDB):

    @classmethod
    def _new_user(cls, _id: str, vendor_type: str) -> JSONDict:
        return {
            "_id": _id,
            "contracts": [],
            "roles": [],
            "vendor_type": vendor_type
        }

    @classmethod
    def get_user(cls, uuid: str) -> Optional[JSONDict]:
        insert_query = {"_id": uuid}
        return cls.get_database().find_one(insert_query)

    @classmethod
    def create_user(cls, uuid: str, vendor_type: str) -> bool:
        insert_query = cls._new_user(uuid, vendor_type)
        cls.get_database().insert_one(insert_query)  # TODO check the response to see if it was actually inserted
        return True

    @classmethod
    def get_database(cls) -> AsyncIOMotorCollection:
        return super().get_database()['users']

    @classmethod
    def get_database_async(cls) -> Collection[MongoMappingType]:
        return super().get_database_async()['users']
