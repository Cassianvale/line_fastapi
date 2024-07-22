# /backend/models/group_model.py

from uuid import UUID
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from backend.apps.model.base_model import BaseUUIDModel


class GroupBase(SQLModel):
    name: str = Field(sa_column_kwargs={"comment": "组名称"}, max_length=50, nullable=False)
    desc: Optional[str] = Field(sa_column_kwargs={"comment": "描述"}, max_length=255, nullable=True)


class Group(BaseUUIDModel, GroupBase, table=True):
    users: List["User"] = Relationship(
        back_populates="group",
        sa_relationship_kwargs={"lazy": "selectin"}
    )