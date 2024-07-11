#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from fastapi import APIRouter
from backend.core.config import settings
from backend.apps.api.v1.endpoints import (
    auth,
    user,
    item,
)

v1 = APIRouter(prefix=settings.API_V1_STR)
v1.include_router(auth.router, prefix="/login", tags=["login"])
# v1.include_router(user.router, prefix="/users", tags=["users"])
v1.include_router(item.router, prefix="/items", tags=["items"])