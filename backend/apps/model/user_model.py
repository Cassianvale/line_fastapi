#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# /backend/models/user_model.py

from datetime import datetime
from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from backend.apps.model.base_model import BaseModel


class UserRoleLink(SQLModel, table=True):
    __tablename__ = 'user_role_link'
    user_id: Optional[int] = Field(default=None, foreign_key="user.id", primary_key=True)
    role_id: Optional[int] = Field(default=None, foreign_key="role.id", primary_key=True)
    user: "User" = Relationship(back_populates="role_links")
    role: "Role" = Relationship(back_populates="user_links")

    create_time: Optional[datetime] = Field(default_factory=datetime.now)
    update_time: Optional[datetime] = Field(default=None)


class Role(BaseModel, table=True):
    __tablename__ = 'role'
    name: str = Field(sa_column_kwargs={"comment": "角色名称"}, max_length=50, nullable=False)
    desc: Optional[str] = Field(sa_column_kwargs={"comment": "描述"}, max_length=255, nullable=True)
    order: Optional[int] = Field(default=0, sa_column_kwargs={"comment": "排序"})
    disabled: bool = Field(default=False, sa_column_kwargs={"comment": "是否禁用"})
    is_admin: bool = Field(default=False, sa_column_kwargs={"comment": "是否为管理员"})

    user_links: list[UserRoleLink] = Relationship(back_populates="role")


if TYPE_CHECKING:
    from backend.apps.model import Item


class User(BaseModel, table=True):
    __tablename__ = 'user'
    username: str = Field(sa_column_kwargs={"comment": "用户名"}, max_length=50, index=True, nullable=True, unique=True)
    hashed_password: str = Field(sa_column_kwargs={"comment": "密码"}, max_length=200, nullable=False)
    avatar: Optional[str] = Field(sa_column_kwargs={"comment": "头像"}, max_length=200, nullable=True)
    nickname: Optional[str] = Field(sa_column_kwargs={"comment": "昵称"}, max_length=50, nullable=True)
    phone: Optional[str] = Field(sa_column_kwargs={"comment": "手机号"}, max_length=11, nullable=True, unique=False)
    email: Optional[str] = Field(sa_column_kwargs={"comment": "邮箱"}, max_length=50, nullable=True)
    is_active: bool = Field(default=True)

    role_links: list[UserRoleLink] = Relationship(back_populates="user")

    # 项目负责人
    items: list["Item"] = Relationship(back_populates="owner")


class UserIn(SQLModel):
    """
    仅管理员能创建用户，创建时分配角色
    """
    role_ids: List[int] = []
    password: str


class UserUpdateBaseInfo(SQLModel):
    """
    更新用户基本信息
    """
    avatar: str
    nickname: str
    phone: str
    email: str


class UserUpdateActive(SQLModel):
    """
    更新用户状态
    """
    is_active: bool
