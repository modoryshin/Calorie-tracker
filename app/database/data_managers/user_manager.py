from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from fastapi import Depends

from app.database.models import User
from app.database import get_db
from app.utils.schemas import UserSchema

#Manages crud operations for user object
class UserRequestManager():
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, user: UserSchema):
        if not user.full_name or user.full_name == '':
            return None, 'Creating a new user requires the full name field'
        exists = await self.session.scalar(select(User).where(User.telegram_id == user.telegram_id))
        if exists:
            return None, f'User with ID {user.telegram_id} already exists'
        else:
            new_user = User(telegram_id=user.telegram_id, full_name='', calorie_macros=user.calorie_macros,
                            carbs_macros=user.carbs_macros, protein_macros=user.protein_macros, fats_macros=user.fats_macros)
            self.session.add(new_user)
            await self.session.commit()
            return user, 'success'

    async def update_user(self, user: UserSchema, user_id: int) -> UserSchema | None:
        upd_user = await self.session.scalar(select(User).where(User.telegram_id == user_id))
        if not upd_user:
            return None
        upd_user.calorie_macros = user.calorie_macros
        upd_user.carbs_macros = user.carbs_macros
        upd_user.protein_macros = user.protein_macros
        upd_user.fats_macros = user.fats_macros
        await self.session.commit()
        return user

    async def fetch_user(self, user_id: Optional[int] = None) -> UserSchema | List[UserSchema] | None:
        if user_id:
            user = await self.session.scalar(select(User).where(User.telegram_id == user_id))
            if not user:
                return None
            return UserSchema(telegram_id=user.telegram_id, full_name=user.full_name, calorie_macros=user.calorie_macros,
                              protein_macros=user.protein_macros, carbs_macros=user.carbs_macros, fats_macros=user.fats_macros)
        else:
            users = await self.session.scalars(select(User))
            if not users.all():
                return None
            
            user_schemas = []
            for user in users.all():
                user_schemas.append(UserSchema(telegram_id=user.telegram_id, full_name=user.full_name, calorie_macros=user.calorie_macros,
                              protein_macros=user.protein_macros, carbs_macros=user.carbs_macros, fats_macros=user.fats_macros))
            return user_schemas

    async def delete_user(self, user_id: int) -> bool:
        user = await self.session.scalar(select(User).where(User.telegram_id == user_id))
        if user:
            await self.session.delete(user)
            await self.session.commit()
            return True
        else:
            return False
        
async def get_user_manager(db: AsyncSession = Depends(get_db)) -> UserRequestManager:
    return UserRequestManager(db)