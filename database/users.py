from motor.motor_asyncio import AsyncIOMotorCollection
from .base_db import BaseDB
from typing import Optional
from utilities.types import JSONDict, MongoMappingType
from typing import Collection


class UsersDB(BaseDB):

    @classmethod
    def empty_user(self) -> JSONDict:
        return {
            "_id": "",
            "contracts": []
        }

    @classmethod
    def get_user(cls, uuid: str) -> Optional[JSONDict]:
        insert_query = {"_id": uuid}
        return cls.get_database().find_one(insert_query)

    @classmethod
    def create_user(cls, uuid: str) -> bool:
        insert_query = cls.empty_user()
        insert_query['_id'] = uuid
        cls.get_database().insert_one(insert_query)
        return True

    @classmethod
    def get_database(cls) -> AsyncIOMotorCollection:
        return super().get_database()['users']

    @classmethod
    def get_database_async(cls) -> Collection[MongoMappingType]:
        return super().get_database_async()['users']
