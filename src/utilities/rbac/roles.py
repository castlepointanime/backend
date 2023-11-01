from typing import List


class Roles:
    CAN_MODIFY_CUSTOMER = "CanEditCustomer"
    CAN_MODIFY_DEVELOPER = "CanEditDeveloper"
    CAN_MODIFY_STAFF = "CanModifyStaff"

    CAN_DELETE_CUSTOMER = "CanDeleteCustomer"
    CAN_DELETE_DEVELOPER = "CanDeleteDeveloper"
    CAN_DELETE_STAFF = "CanDeleteStaff"

    ARTIST_REVIEWER = "ArtistReviewer"
    DEALER_REVIEWER = "DealerReviewer"

    CAN_CHANGE_GROUPS = "CanChangeGroup"

    @classmethod
    def get_default_customer_roles(cls) -> List[str]:
        return []

    @classmethod
    def get_default_staff_roles(cls) -> List[str]:
        return []

    @classmethod
    def get_default_developer_roles(cls) -> List[str]:
        return [cls.CAN_MODIFY_STAFF, cls.CAN_CHANGE_GROUPS]

    @classmethod
    def get_all(cls) -> List[str]:
        return [cls.CAN_MODIFY_CUSTOMER, cls.CAN_MODIFY_DEVELOPER, cls.CAN_MODIFY_STAFF,
                cls.CAN_DELETE_CUSTOMER, cls.CAN_DELETE_DEVELOPER, cls.CAN_DELETE_STAFF,
                cls.ARTIST_REVIEWER, cls.DEALER_REVIEWER, cls.CAN_CHANGE_GROUPS]
