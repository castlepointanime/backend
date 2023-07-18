from typing import List
import calendar

EMAIL_REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
DATE_FORMAT_STRING = "%Y-%m-%d"
CONTRACT_TYPES + ['artist', 'dealer']
VALID_MONTH_NAMES : List[str] = calendar.month_name[1:] # index 0 is an empty string

class Validation:

    @classmethod
    def is_valid_email(cls,  email : str) -> bool:
        return re.fullmatch(EMAIL_REGEX, email)
        
    @classmethod
    def is_valid_date(cls, shortened_year: int, month: int, day: int) -> bool:
        #shortened_year is the last 2 digits of a year (ex: 2022 -> 22)
        # TODO: change in 2100 :)
        if not isinstance(shortened_year, int):
            return False
        if not isinstance(month, int):
            return False
        if not isinstance(day, int):
            return False
        try:
            datetime.datetime.strptime(DATE_FORMAT_STRING, f"20{shortened_year}-{month}-{day}")
            return True
        except ValueError:
            return False

    @classmethod
    def is_valid_phone_number(cls, phone_number: int) -> bool:
        #phone number can only have 10 digits
        return type(phone_number) == int and 0 < phone_number < 9_999_999_999

    @classmethod
    def is_valid_contract_type(cls, contract_type: str) -> bool:
        return contract_type in CONTRACT_TYPES

    @classmethod
    def is_valid_month_name(cls, month_name: str) -> bool:
        return month_name in VALID_MONTH_NAMES

    @classmethod
    def is_valid_helper_badge_quantity(cls, helper_badge_quantity: int) -> bool:
        return type(helper_badge_quantity) == int and 0 < helper_badge_quantity <= 2 # cannot have more than 2 helper badges

    @classmethod
    def is_valid_additional_chairs_quantity(cls, additional_chairs_quantity: int) -> bool:
        return type(additional_chairs_quantity) == int and 0 < additional_chairs_quantity <= 2 # cannot have more than 2 additional chairs
        