#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from typing import Any
from fastapi import APIRouter
from backend.core.security import CurrentSession, CurrentUser
from backend.apps.model import Item, ItemCreate, ItemPublic

router = APIRouter()


@router.post("/", response_model=ItemPublic)
def create_item(
    *, session: CurrentSession, current_user: CurrentUser, item_in: ItemCreate
) -> Any:
    # 创建新的Item实例并更新owner_id为当前用户id
    item = Item.model_validate(item_in, update={"owner_id": current_user.id})
    # 添加数据库会话中
    session.add(item)
    session.commit()
    session.refresh(item)  # 刷新实例
    return item
