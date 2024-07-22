from fastapi import APIRouter
from sqlalchemy_crud_plus import CRUDPlus
from backend.apps.model import Role

class CRUDUser(CRUDPlus[Role]):
    async def get_role_by_name():
        pass
    
    async def add_role_to_user():
        pass