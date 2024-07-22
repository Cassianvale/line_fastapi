#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# /backend/models/role_model.py

from uuid import UUID
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from backend.apps.model.base_model import BaseUUIDModel


class RoleBase(SQLModel):
    name: str = Field(sa_column_kwargs={"comment": "角色名称"}, max_length=50, nullable=False)
    desc: Optional[str] = Field(sa_column_kwargs={"comment": "描述"}, max_length=255, nullable=True)
    # order: Optional[int] = Field(default=0, sa_column_kwargs={"comment": "排序"})
    disabled: bool = Field(default=False, sa_column_kwargs={"comment": "是否禁用"})
    is_admin: bool = Field(default=False, sa_column_kwargs={"comment": "是否为管理员"})


class Role(BaseUUIDModel, RoleBase, table=True):
    users: List["User"] = Relationship(back_populates="role")
    follower_count: int = Field(default=0, sa_column_kwargs={"comment": "绑定该角色的用户数量"})