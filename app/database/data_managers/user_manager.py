from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from fastapi import Depends
from datetime import datetime

from app.database.models import User, Meal
from app.database import get_db
from app.utils.schemas import UserSchema, MacrosSchema, MealSchema

#Manages crud operations for user object
class UserRequestManager():
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, user: UserSchema) -> UserSchema | None:
        exists = await self.session.scalar(select(User).where(User.telegram_id == user.telegram_id))
        if exists:
            return None
        else:
            new_user = User(telegram_id=user.telegram_id, full_name='', calorie_macros=user.calorie_macros,
                            carbs_macros=user.carbs_macros, protein_macros=user.protein_macros, fats_macros=user.fats_macros)
            self.session.add(new_user)
            await self.session.commit()
            await self.session.refresh(new_user)
            return UserSchema.model_validate(new_user)

    async def update_user(self, user: MacrosSchema, user_id: int) -> UserSchema | None:
        upd_user = await self.session.scalar(select(User).where(User.telegram_id == user_id))
        if not upd_user:
            return None
        upd_user.calorie_macros = user.calorie_macros
        upd_user.carbs_macros = user.carbs_macros
        upd_user.protein_macros = user.protein_macros
        upd_user.fats_macros = user.fats_macros
        await self.session.commit()
        await self.session.refresh(upd_user)
        return UserSchema.model_validate(upd_user)

    async def fetch_user(self, user_id: Optional[int] = None) -> UserSchema | List[UserSchema] | None:
        if user_id:
            user = await self.session.scalar(select(User).where(User.telegram_id == user_id))
            if not user:
                return None
            return UserSchema.model_validate(user)
        else:
            users = await self.session.scalars(select(User))
            if not users.all():
                return None
            
            user_schemas = []
            for user in users.all():
                user_schemas.append(UserSchema.model_validate(user))
            return user_schemas

    async def delete_user(self, user_id: int) -> bool:
        user = await self.session.scalar(select(User).where(User.telegram_id == user_id))
        if user:
            await self.session.delete(user)
            await self.session.commit()
            return True
        else:
            return False
    
    async def get_user_status(self, user_id: int, timestamp: datetime) -> MacrosSchema:
        tstmp_low = timestamp
        tstmp_high = timestamp.replace(hour=23, minute=59, second=59)
        result = await self.session.scalars(select(Meal).where(Meal.user_id == user_id and (
            Meal.timestamp >= tstmp_low and Meal.timestamp <= tstmp_high)).order_by(Meal.timestamp.desc()))
        meals: List[MealSchema] = result.all()
        result = await self.session.scalar(select(User).where(User.telegram_id == user_id))
        user_macros: MacrosSchema = MacrosSchema(**result.__dict__)
        if not user_macros:
            return None

        for meal in meals:
            user_macros.calorie_macros -= meal.calorie_count
            user_macros.carbs_macros -= meal.carbs_count
            user_macros.protein_macros -= meal.protein_count
            user_macros.fats_macros -= meal.fats_count
        return user_macros

async def get_user_manager(db: AsyncSession = Depends(get_db)) -> UserRequestManager:
    return UserRequestManager(db)