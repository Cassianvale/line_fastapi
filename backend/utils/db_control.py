#!/usr/bin/env python
# -*- coding: utf-8 -*-
# /backend/utils/db_control.py

import sys
from typing import Any, AsyncGenerator
from fastapi import Depends
from uuid import uuid4
from sqlmodel import SQLModel
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from typing_extensions import Annotated
from backend.core.config import settings
from backend.utils.log_control import logger


def create_engine_and_session(url: str | URL):
    try:
        # 数据库引擎
        engine = create_async_engine(url, echo=settings.MYSQL_ECHO, future=True, pool_pre_ping=True)
    except Exception as e:
        logger.error('❌ 数据库链接失败 {}', e)
        sys.exit()
    else:
        db_session = async_sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
        return engine, db_session


def SQLALCHEMY_DATABASE_URL() -> str:
    """生成数据库连接URL"""
    return f"mysql+asyncmy://{settings.MYSQL_USER}:{settings.MYSQL_PASSWORD}@{settings.MYSQL_HOST}:{settings.MYSQL_PORT}/{settings.MYSQL_DB}"


async_engine, async_db_session = create_engine_and_session(SQLALCHEMY_DATABASE_URL())


async def get_db():
    """session 生成器"""
    async with async_db_session() as session:
        try:
            yield session
        except Exception as se:
            await session.rollback()
            raise se
        finally:
            await session.close()


# Session依赖注入,获取数据库会话
CurrentSession = Annotated[AsyncSession, Depends(get_db)]


async def create_table():
    """创建数据库表"""
    async with async_engine.begin() as coon:
        await coon.run_sync(SQLModel.metadata.create_all)


def uuid4_str() -> str:
    """数据库引擎 UUID 类型兼容性解决方案"""
    return str(uuid4())
