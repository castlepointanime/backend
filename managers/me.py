from database import UsersDB


class MeManager():

    async def create_user(self, user_id: str, vendor_type: str) -> bool:
        return await UsersDB.create_user(user_id, vendor_type)
