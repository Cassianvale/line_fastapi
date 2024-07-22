#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# /backend/models/item_model.py

from uuid import UUID
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from backend.apps.model.base_model import BaseUUIDModel


class ProjectBase(SQLModel):
    title: str = Field(index=True, max_length=50, nullable=False, default=None, sa_column_kwargs={"comment": "标题"})
    description: Optional[str] = Field(max_length=255, nullable=True, sa_column_kwargs={"comment": "描述"})


class Project(BaseUUIDModel, ProjectBase, table=True):
    owner_id: Optional[UUID] = Field(foreign_key="user.id", default=None, sa_column_kwargs={"comment": "项目拥有者"})
    owner: Optional["User"] = Relationship(back_populates="projects")
