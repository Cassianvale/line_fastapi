#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from datetime import timedelta
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from backend.utils.db_control import CurrentSession
from fastapi import APIRouter
from backend.core import security
from backend.core.config import settings
from backend.utils.response_control import ApiResponse
from sqlmodel.ext.asyncio.session import AsyncSession

router = APIRouter()


# 登录接口
@router.post("/")
def login_access_token(
    session: CurrentSession, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):

    user = security.authenticate_user(
        session=session, username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户名或密码错误")
    elif not user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户已被禁用")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        user.id, expires_delta=access_token_expires
    )

    return ApiResponse(data={"access_token": access_token, "token_type": "bearer"}, msg="登录成功")

# 登出接口
@router.post("/logout")
def logout_access_token():
    return ApiResponse(msg="登出成功")