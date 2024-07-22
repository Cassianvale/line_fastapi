#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# /backend/models/user_model.py

from uuid import UUID
from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from backend.apps.model.base_model import BaseUUIDModel


class UserBase(SQLModel):
    username: str = Field(sa_column_kwargs={"comment": "用户名"}, max_length=50, index=True, nullable=True, unique=True)
    phone: Optional[str] = Field(sa_column_kwargs={"comment": "手机号"}, max_length=11, nullable=True, unique=False)
    avatar: Optional[str] = Field(sa_column_kwargs={"comment": "头像"}, max_length=200, nullable=True)
    nickname: Optional[str] = Field(sa_column_kwargs={"comment": "昵称"}, max_length=50, nullable=True)
    email: Optional[str] = Field(sa_column_kwargs={"comment": "邮箱"}, max_length=50, nullable=True)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)


class User(BaseUUIDModel, UserBase, table=True):
    hashed_password: str = Field(sa_column_kwargs={"comment": "密码"}, max_length=200, nullable=False)
    role_id: UUID = Field(foreign_key="role.id")
    group_id: UUID = Field(foreign_key="group.id")
    
    # 多对一
    role: Optional["Role"] = Relationship(
        back_populates="users", 
        sa_relationship_kwargs={"lazy": "joined"}
    )
    
    # 多对一
    group: Optional["Group"] = Relationship(
        back_populates="users",
        sa_relationship_kwargs={"lazy": "joined"}
    )
    
    # 一对多
    projects: List["Project"] = Relationship(
        back_populates="owner",
        sa_relationship_kwargs={"lazy": "selectin"}
    )


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
