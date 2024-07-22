#!/usr/bin/env python
# -*- coding: utf-8 -*-
# /core/database.py

from uuid import UUID
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel as _SQLModel, Field
from sqlalchemy.orm import declared_attr
from backend.utils.uuid6 import uuid7


class SQLModel(_SQLModel):
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

class BaseUUIDModel(SQLModel):
    id: UUID = Field(
        default_factory=uuid7,
        primary_key=True,
        index=True,
        nullable=False,
    )
    created_time: Optional[datetime] = Field(default_factory=datetime.utcnow,
                                             sa_column_kwargs={"comment": "创建时间"})
    updated_time: Optional[datetime] = Field(default_factory=datetime.utcnow,
                                             sa_column_kwargs={"onupdate": datetime.utcnow, "comment": "更新时间"})
    delete_time: Optional[datetime] = Field(default=None, sa_column_kwargs={"comment": "删除时间"})
    is_delete: Optional[bool] = Field(default=False, sa_column_kwargs={"comment": "是否删除"})
