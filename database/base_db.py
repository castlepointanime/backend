from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from config.env import MONGO_URI, MONGO_DB_NAME
import logging
from pymongo import MongoClient
import pymongo.database
from typing import Optional, Union
from utilities.types import MongoMappingType


class BaseDB:

    async_client: Optional[AsyncIOMotorClient] = None
    client: Optional[MongoClient[MongoMappingType]] = None

    @classmethod
    def _get_client_async(cls) -> AsyncIOMotorClient:
        if not cls.async_client:
            cls.async_client = AsyncIOMotorClient(MONGO_URI)
            cls._verify_connection(cls.async_client)
        return cls.async_client

    @classmethod
    def _get_client(cls) -> MongoClient[MongoMappingType]:
        if not cls.client:
            assert MONGO_URI is not None, "No mongo uri in environment"
            cls.client = MongoClient(MONGO_URI)
            cls._verify_connection(cls.client)
        return cls.client

    @classmethod
    def _verify_connection(cls, client: Union[MongoClient[MongoMappingType], AsyncIOMotorClient]) -> None:
        try:
            client.server_info()
        except Exception as e:
            logging.critical("Cannot connect to db.")
            raise e

    @classmethod
    def get_database_async(cls) -> AsyncIOMotorDatabase:
        assert type(MONGO_DB_NAME) == str, "No mongo db name in environment"
        return cls._get_client_async()[MONGO_DB_NAME]

    @classmethod
    def get_database(cls) -> pymongo.database.Database[MongoMappingType]:
        assert type(MONGO_DB_NAME) == str, "No mongo db name in environment"
        return cls._get_client()[MONGO_DB_NAME]
