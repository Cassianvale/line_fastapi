#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# /backend/models/item_model.py

from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from backend.apps.model.base_model import BaseModel
from backend.apps.model.user_model import User


class Item(BaseModel, table=True):
    title: str = Field(sa_column_kwargs={"comment": "标题"}, max_length=50, nullable=False)
    description: Optional[str] = Field(sa_column_kwargs={"comment": "描述"}, max_length=255, nullable=True)
    owner_id: int = Field(default=None, foreign_key="user.id", nullable=False, sa_column_kwargs={"comment": "项目拥有者"})
    owner: Optional[User] = Relationship(back_populates="items")


class ItemBase(SQLModel):
    title: str
    description: str | None = None


class ItemCreate(ItemBase):
    title: str


class ItemUpdate(ItemBase):
    title: str | None = None


class ItemPublic(ItemBase):
    id: int
    owner_id: int

