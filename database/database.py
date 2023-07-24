from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection
from config.env import MONGO_URI, MONGO_DB_NAME
import logging
from pymongo import MongoClient
import pymongo.database
from pymongo.collection import Collection
from typing import Optional


class Database:

    async_client: Optional[AsyncIOMotorClient] = None
    client: Optional[MongoClient] = None

    @classmethod
    def _get_client_async(cls) -> AsyncIOMotorClient:
        if not cls.async_client:
            cls.async_client = AsyncIOMotorClient(MONGO_URI)
            cls._verify_connection(cls.async_client)
        return cls.async_client

    @classmethod
    def _get_client(cls) -> MongoClient:
        if not cls.client:
            cls.client = MongoClient(MONGO_URI)
            cls._verify_connection(cls.client)
        return cls.client

    @classmethod
    def _get_database_async(cls) -> AsyncIOMotorDatabase:
        return cls._get_client_async()[MONGO_DB_NAME]

    @classmethod
    def _get_database(cls) -> pymongo.database.Database:
        return cls._get_client()[MONGO_DB_NAME]

    @classmethod
    def _verify_connection(cls, client: AsyncIOMotorClient) -> None:
        try:
            client.server_info()
        except Exception as e:
            logging.critical("Cannot connect to db.")
            raise e

    @classmethod
    def get_users_database(cls) -> AsyncIOMotorCollection:
        return cls._get_database()['users']

    @classmethod
    def get_users_database_async(cls) -> Collection:
        return cls._get_database_async()['users']
