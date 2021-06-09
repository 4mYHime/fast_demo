
from typing import Optional
from pydantic import BaseModel

from api.common.schemas_base import RespBase


class Token(BaseModel):
    token: str


class TokenPayload(BaseModel):
    sub: Optional[str] = None


class RespToken(RespBase):
    # 认证响应模型
    data: Token
