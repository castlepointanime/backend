from database import UsersDB


class MeManager():

    async def create_user(self, user_id: str, username: str, vendor_type: str) -> bool:
        return await UsersDB.create_user(user_id, username, vendor_type)
