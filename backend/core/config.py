#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# /backend/core/config.py

import os
from typing import Text
from functools import lru_cache
from typing import Literal
from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


def root_path():
    """获取根路径"""
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return path


def ensure_path_sep(path: Text) -> Text:
    """兼容 windows 和 linux 不同环境的操作系统路径 """
    if "/" in path:
        path = os.sep.join(path.split("/"))

    if "\\" in path:
        path = os.sep.join(path.split("\\"))

    return root_path() + path


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ensure_path_sep("\\.env"),
        env_file_encoding='utf-8',
        case_sensitive=True)

    # Env Config
    ENVIRONMENT: Literal['dev', 'pro']

    TITLE: str = 'This a project name.'
    DESCRIPTION: str = 'This a description.'
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    DOCS_URL: str | None = f'{API_V1_STR}/docs'
    REDOCS_URL: str | None = f'{API_V1_STR}/redocs'
    OPENAPI_URL: str | None = f'{API_V1_STR}/openapi'

    @model_validator(mode='before')
    @classmethod
    def validator_api_url(cls, values):
        if values['ENVIRONMENT'] == 'pro':
            values['OPENAPI_URL'] = None
        return values
    
    # Uvicorn Config
    UVICORN_HOST: str = '127.0.0.1'
    UVICORN_PORT: int = 8000
    UVICORN_RELOAD: bool = True

    # Token Config
    # SECRET_KEY: str = secrets.token_urlsafe(32)
    SECRET_KEY: str
    TOKEN_ALGORITHM: str = 'HS256'
    TOKEN_URL_SWAGGER: str = f'{API_V1_STR}/auth/login'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 1440
    ACCESS_TOKEN_CACHE_MINUTES: int = 30

    # Env MySQL
    MYSQL_HOST: str
    MYSQL_PORT: int
    MYSQL_DB: str
    MYSQL_USER: str
    MYSQL_PASSWORD: str

    MYSQL_ECHO: bool = False
    MYSQL_DATABASE: str = 'fastsql'
    MYSQL_CHARSET: str = 'utf8mb4'

    # Env Redis
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DATABASE: int
    REDIS_PASSWORD: str
    REDIS_TIMEOUT: int = 10

    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = "123456"

    # 中间件
    MIDDLEWARE_CORS: bool = True
    MIDDLEWARE_GZIP: bool = True
    MIDDLEWARE_ACCESS: bool = False
    
    # DateTime
    DATETIME_TIMEZONE: str = 'Asia/Shanghai'
    DATETIME_FORMAT: str = '%Y-%m-%d %H:%M:%S'



@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
