"""
响应基类模板
"""
from typing import Union, Any

from pydantic import BaseModel, Field


class BaseSchema(BaseModel):
    code: int = Field(default=None, example=200, description="业务响应码")
    message: str = Field(default=None, example="业务提示码", description="业务提示码")
    data: Union[str, dict, Any] = Field(default=None, description="业务信息体")


class LoginSchema(BaseSchema):
    data: dict = Field(default=None, description="业务信息体",
                       example=dict(access_token="access_token",
                                    expires_delta=50,
                                    third_username="IM/视频 用户名",
                                    sig="1231231",
                                    is_freshman=True,
                                    is_broadcaster=False))
