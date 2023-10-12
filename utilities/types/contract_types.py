from typing import Dict, Union
from pydantic import BaseModel, Field
from .fields import phone_number

Helper = Dict[str, Union[str, int]]


class HelperModel(BaseModel):
    name: str = Field(alias="name", examples=["Bob"])
    phone_number: int = phone_number("phoneNumber")
