#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# /core/initialize.py


import subprocess
from contextlib import asynccontextmanager
from enum import Enum

from fastapi import FastAPI
from fastapi_pagination import add_pagination
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select as sql_select
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware

from backend.apps.api import v1 as route
from backend.apps.model import Role, User, UserRoleLink
from backend.core import security
from backend.core.config import root_path, settings
from backend.utils.db_control import create_table, get_db
from backend.utils.exception_handler import register_exception
from backend.utils.health_check import ensure_unique_route_names
from backend.utils.log_control import AccessMiddleware, logger
from backend.utils.redis_client import redis_client


@asynccontextmanager
async def get_db_context():
    async for session in get_db():
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

@asynccontextmanager
async def register_init(app: FastAPI):
    print("初始化数据中...")
    await create_table()
    await redis_client.open()

    async with get_db_context() as session:
        print("新建角色中...")
        await InitializeData.create_roles(session)
        print("添加管理员角色中...")
        super_user = await InitializeData.create_super_user(session)
        if super_user:
            await InitializeData.bind_super_user_role(session, super_user)
    yield

    # 关闭 redis 连接
    await redis_client.close()
    
def register_app() -> FastAPI:
    app = FastAPI(
        title=settings.TITLE,
        version=settings.VERSION,
        description=settings.DESCRIPTION,
        docs_url=settings.DOCS_URL,
        redoc_url=settings.REDOCS_URL,
        openapi_url=settings.OPENAPI_URL,
        lifespan=register_init,
    )
    # 中间件
    register_middleware(app)
    # 路由
    register_router(app)
    # 分页
    register_page(app)
    # 全局异常处理
    register_exception(app)
    return app

def register_router(app: FastAPI):
    """
    路由&限流
    """
    app.include_router(route)
    ensure_unique_route_names(app)


def register_middleware(app) -> None:
    # gzip
    if settings.MIDDLEWARE_GZIP:
        app.add_middleware(GZipMiddleware)
    # 接口访问日志
    if settings.MIDDLEWARE_ACCESS:
        app.add_middleware(AccessMiddleware)
    # 跨域
    if settings.MIDDLEWARE_CORS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=['*'],
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*'],
        )


def register_page(app: FastAPI):
    """
    分页查询
    """
    add_pagination(app)


class Environment(str, Enum):
    dev = "dev"
    pro = "pro"


class InitializeData:

    @classmethod
    async def create_roles(cls, session: AsyncSession):
        """
        Create initial roles in the system
        """
        roles = [
            Role(name="admin", desc="This the Admin role", is_admin=True),
            Role(name="manager", desc="Manager role"),
            Role(name="user", desc="User role")
        ]

        for role in roles:
            stmt = sql_select(Role).where(Role.name == role.name)
            existing_role = (await session.execute(stmt)).scalars().first()
            if not existing_role:
                session.add(role)
                await session.commit()
                logger.info(f"角色 '{role.name}' 已被创建")
                
    @classmethod
    async def create_super_user(cls, session: AsyncSession):
        # 从 settings 中获取超级管理员账号和密码
        admin_username = settings.ADMIN_USERNAME
        admin_password = settings.ADMIN_PASSWORD

        # 检查是否已经存在超级管理员用户
        stmt = sql_select(User).where(User.username == admin_username)
        super_user = (await session.execute(stmt)).scalars().first()
        if super_user:
            logger.info(f"超级管理员用户 '{super_user.username}' 已存在.")
            return None

        # 如果不存在超级管理员，创建一个
        hashed_password = security.hash_password(admin_password)
        new_user = User(username=admin_username, hashed_password=hashed_password, is_active=True)
        session.add(new_user)
        await session.commit()
        logger.info(f"超级管理员 '{admin_username}' 已被创建")
        return new_user

    @classmethod
    async def bind_super_user_role(cls, session: AsyncSession, super_user: User):
        """
        绑定超级管理员角色
        """
        super_admin_role = await session.execute(sql_select(Role).where(Role.name == "admin"))
        super_admin_role = super_admin_role.scalars().first()
        if super_admin_role:
            user_role_link = UserRoleLink(user_id=super_user.id, role_id=super_admin_role.id)
            session.add(user_role_link)
            await session.commit()
            logger.info(f"超级管理员: '{super_user.username}' 绑定角色: '{super_admin_role.name}'")

    @classmethod
    def migrate_model(cls, env: Environment = Environment.dev):
        """
        模型迁移映射到数据库
        """
        # 生成迁移文件
        print("生成迁移文件")
        subprocess.check_call(
            ['alembic', '--name', f'{env.value}', 'revision', '--autogenerate', '-m', f'{settings.VERSION}'],
            cwd=root_path)
        print("迁移文件映射到数据库")
        # 将迁移文件映射到数据库
        subprocess.check_call(['alembic', '--name', f'{env.value}', 'upgrade', 'head'], cwd=root_path)
        logger.info(f"环境：{env}  {settings.VERSION} 数据库表迁移完成")
