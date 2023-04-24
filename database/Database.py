from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection
import env
import logging
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection

class Database:

    async_client : AsyncIOMotorClient = None
    client : MongoClient = None
    
    @classmethod
    def _get_client_async(cls) -> AsyncIOMotorClient:
        if not cls.async_client:
            cls.async_client = AsyncIOMotorClient(env.MONGO_URI)
            cls._verify_connection(cls.async_client)
        return cls.async_client

    @classmethod
    def _get_client(cls) -> MongoClient:
        if not cls.client:
            cls.client = MongoClient(env.MONGO_URI)
            cls._verify_connection(cls.client)
        return cls.client
    
    @classmethod
    def _get_database_async(cls) -> AsyncIOMotorDatabase:
        return cls._get_client_async()[env.MONGO_DB_NAME]
    
    @classmethod
    def _get_database(cls) -> Database:
        return cls._get_client()[env.MONGO_DB_NAME]

    @classmethod
    def _verify_connection(cls, client) -> None:
        try:
            client.server_info()
        except Exception as e:
            logging.critical(f"Cannot connect to db.")
            logging.exception(e)

    @classmethod
    def get_users_database(cls) -> AsyncIOMotorCollection:
        return cls._get_database()['users']

    @classmethod
    def get_users_database_async(cls) -> Collection:
        return cls._get_database_async()['users']