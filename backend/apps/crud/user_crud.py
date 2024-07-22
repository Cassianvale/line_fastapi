from fastapi import APIRouter
from backend.apps.model import User
from sqlmodel import select
from sqlalchemy_crud_plus import CRUDPlus
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter()


class CRUDUser(CRUDPlus[User]):
    async def get_user_by_id(self, db: AsyncSession, user_id: int) -> User | None:
        return await self.select_model_by_id(db, user_id)
    
    async def get_user_by_username(self, db: AsyncSession, username: str) -> User | None:
        return await self.select_model_by_column(db, 'username', username)

