#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from typing import Any, Optional
from datetime import datetime, timedelta

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from authlib.jose import jwt, JoseError
from passlib.context import CryptContext
from pydantic import ValidationError
from sqlmodel import Session, select
from typing_extensions import Annotated

from backend.apps.model import User
from backend.core.config import settings
from backend.utils.db_control import CurrentSession
from backend.utils.errors import TokenError, AuthorizationError


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_schema = OAuth2PasswordBearer(tokenUrl=settings.TOKEN_URL_SWAGGER)


def create_access_token(subject: str | Any, expires_delta: Optional[timedelta] = None) -> str:
    """
    生成加密 token
    """
    expire = datetime.now() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.TOKEN_ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    密码校验
    :param plain_password: 需要验证的密码
    :param hashed_password: 要比较的hash密码
    :return: 比较结果
    """
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    """
    使用 hash 算法加密密码

    :param password: 密码
    :return: 加密后的密码
    """
    return pwd_context.hash(password)


async def get_current_user(db: CurrentSession, token: str = Depends(oauth2_schema)) -> User:
    """
    通过 token 获取当前用户

    :param db:
    :param token:
    :return:
    """
    try:
        # 解密token
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.TOKEN_ALGORITHM])
        user_id = payload.get('sub')
        if not user_id:
            raise TokenError
    except (JoseError, ValidationError):
        raise TokenError
    user = await User.get_user_by_id(db, user_id)
    if not user:
        raise TokenError
    return user


async def get_current_active_superuser(current_user: User) -> User:
    """
    验证当前用户是否为超级用户
    """
    if not current_user.is_superuser:
        raise AuthorizationError
    return current_user


# 用户依赖注入
CurrentUser = Annotated[User, Depends(get_current_user)]
# 权限依赖注入
DependsJwtUser = Depends(get_current_user)
