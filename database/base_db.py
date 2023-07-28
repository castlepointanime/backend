from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection
from config.env import MONGO_URI, MONGO_DB_NAME
import logging
from pymongo import MongoClient
import pymongo.collection
import pymongo.database
from typing import Optional, Union, List
from utilities.types import MongoMappingType, JSONDict


class BaseDB:

    async_client: Optional[AsyncIOMotorClient] = None  # type: ignore[no-any-unimported]
    client: Optional[MongoClient[MongoMappingType]] = None

    @classmethod
    def _get_client_async(cls) -> AsyncIOMotorClient:  # type: ignore[no-any-unimported]
        if not cls.async_client:
            cls.async_client = AsyncIOMotorClient(MONGO_URI)
            cls._verify_connection(cls.async_client)
        return cls.async_client

    @classmethod
    def _get_client(cls) -> MongoClient[MongoMappingType]:
        if not cls.client:
            cls.client = MongoClient(MONGO_URI)
            cls._verify_connection(cls.client)
        return cls.client

    @classmethod
    def _verify_connection(cls, client: Union[MongoClient[MongoMappingType], AsyncIOMotorClient]) -> None:  # type: ignore[no-any-unimported]
        try:
            client.server_info()
        except Exception as e:
            logging.critical("Cannot connect to db.")
            raise e

    @classmethod
    def get_database_async(cls) -> AsyncIOMotorDatabase:  # type: ignore[no-any-unimported]
        return cls._get_client_async()[MONGO_DB_NAME]

    @classmethod
    def get_database(cls) -> pymongo.database.Database[MongoMappingType]:
        return cls._get_client()[MONGO_DB_NAME]

    @classmethod
    def get_random(cls, collection: Union[pymongo.collection.Collection[MongoMappingType], AsyncIOMotorCollection], count: int, query: JSONDict) -> List[MongoMappingType]:  # type: ignore[no-any-unimported]
        results = []

        aggregate_query = [
            {"$match": query},
            {"$sample": {"size": count}}
            ]
        it = collection.aggregate(aggregate_query)
        for doc in it:
            results.append(doc)
        return results
