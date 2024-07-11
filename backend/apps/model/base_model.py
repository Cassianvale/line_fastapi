#!/usr/bin/env python
# -*- coding: utf-8 -*-
# /core/database.py

from datetime import datetime
from typing import Optional
from sqlalchemy.orm import declared_attr
from sqlmodel import SQLModel as _SQLModel, Field


class SQLModel(_SQLModel):
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class BaseModel(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    created_time: Optional[datetime] = Field(default_factory=datetime.utcnow,
                                             sa_column_kwargs={"comment": "创建时间"})
    updated_time: Optional[datetime] = Field(default_factory=datetime.utcnow,
                                             sa_column_kwargs={"onupdate": datetime.utcnow, "comment": "更新时间"})
    delete_time: Optional[datetime] = Field(default=None, sa_column_kwargs={"comment": "删除时间"})
    is_delete: Optional[bool] = Field(default=False, sa_column_kwargs={"comment": "是否删除"})

