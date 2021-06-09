# coding=utf-8

from fastapi import APIRouter, Depends, Body, Request
from sqlalchemy.orm import Session

from api.api_v1.auth.crud import curd_user
from api.api_v1.auth.schemas import resp_base_schema
from api.api_v1.auth.schemas import user_schema
from api.utils import response_code
from database.session import get_db

router = APIRouter()


@router.post(
    'act/user/login',
    summary="用户邮箱注册登录",
    response_model=resp_base_schema.LoginSchema)
async def user_login(
        *,
        db: Session = Depends(get_db),
        request: Request,
        post_data: user_schema.ForeignLoginSchema = Body(default=None, description="登录传的信息",
                                                         example=dict(
                                                             email="13456993881@163.com",
                                                             password="123456"))
):
    if not curd_user.check_password(password=post_data.password):
        return response_code.resp_4000(data="Account and password do not match", db=db)
    return response_code.resp_200(data={})
