"""

"""
from typing import Union
from pydantic import BaseModel


class RespBase(BaseModel):
    code: int
    message: str
    data: Union[dict, list, str]
