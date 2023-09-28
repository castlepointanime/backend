from pydantic import Field
from config import Config
from enum import Enum

config = Config()
phone_number_max = config.get_contract_limit("phone_number_max")
phone_number_min = config.get_contract_limit("phone_number_min")


def phone_number(alias: str) -> int:
    # This is technically a pydantic.fields.FieldInfo, but we will trick mypy so it's callers can be defined correctly
    result: int = Field(alias=alias, ge=phone_number_max, le=phone_number_min, examples=['11234567890'])
    return result


class VendorTypeEnum(Enum):
    artist = 'artist'
    dealer = 'dealer'
