from typing import List


class Groups:
    CUSTOMER = "Customer"
    STAFF = "Staff"
    DEVELOPER = "Developer"

    @classmethod
    def get_all(cls) -> List[str]:
        return [cls.CUSTOMER, cls.STAFF, cls.DEVELOPER]
