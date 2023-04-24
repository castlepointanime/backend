from .Database import Database
import uuid

class Users:

    @classmethod
    def empty_user() -> dict:
        return {
            "_id": "",
            "contracts": []
        }

    @classmethod
    def get_user(cls, uuid: str) -> dict:
        insert_query = {"_id": uuid}
        return Database.get_users_database().find_one(insert_query)

    @classmethod
    def create_user(cls, uuid: str) -> bool:
        insert_query = cls.empty_user()
        insert_query['_id'] = uuid
        Database.get_users_database().insert_one(insert_query)
        return True
