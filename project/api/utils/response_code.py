"""
定义返回的状态

# 看到文档说这个orjson 能压缩性能(squeezing performance)
https://fastapi.tiangolo.com/advanced/custom-response/#use-orjsonresponse

It's possible that ORJSONResponse might be a faster alternative.

# 安装
pip install --upgrade orjson

测试了下，序列化某些特殊的字段不友好，比如小数
TypeError: Type is not JSON serializable: decimal.Decimal
"""
from typing import Union, Any

from fastapi import status
from fastapi.responses import JSONResponse, Response  # , ORJSONResponse
from sqlalchemy.orm import Session


def resp_200(*, data: Union[list, dict, str, Any] = None, message: str = "Success", db: Session = None):
    if db:
        db.close()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'code': 200,
            'message': message,
            'data': data,
        }
    )


def resp_4000(*, data: str = None, message: str = "BAD REQUEST", db: Session = None) -> Response:
    if db:
        db.close()
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            'code': 4000,
            'message': message,
            'data': data,
        }
    )
