from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection
from config.env import MONGO_URI, MONGO_DB_NAME
from typing import Optional, List
from utilities.types import MongoMappingType, JSONDict


class BaseDB:

    client: Optional[AsyncIOMotorClient] = None  # type: ignore[no-any-unimported]

    @classmethod
    def _get_client(cls) -> AsyncIOMotorClient:  # type: ignore[no-any-unimported]
        if not cls.client:
            cls.client = AsyncIOMotorClient(MONGO_URI)
            cls._verify_connection(cls.client)
        return cls.client

    @classmethod
    def _verify_connection(cls, client: AsyncIOMotorClient) -> None:  # type: ignore[no-any-unimported]
        client.server_info()

    @classmethod
    def get_database(cls) -> AsyncIOMotorDatabase:  # type: ignore[no-any-unimported]
        return cls._get_client()[MONGO_DB_NAME]

    # TODO this needs to be reworked
    @classmethod
    async def get_random(cls, collection: AsyncIOMotorCollection, count: int, query: JSONDict) -> List[MongoMappingType]:  # type: ignore[no-any-unimported]
        results = []

        aggregate_query = [
            {"$match": query},
            {"$sample": {"size": count}}
            ]
        it = collection.aggregate(aggregate_query)
        async for doc in it:
            results.append(doc)
        return results
