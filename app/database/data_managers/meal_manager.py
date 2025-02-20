from sqlalchemy import select, desc, and_
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination.ext.sqlalchemy import paginate
from typing import Optional, List, Any
from datetime import datetime
from fastapi import Depends
from fastapi_pagination import LimitOffsetPage, Page
from fastapi_pagination.ext.sqlalchemy import paginate

from app.database.models import Meal, User
from app.database import get_db
from app.utils.schemas import MealSchema

#Manages crud operations for user object
class MealRequestManager():
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_meal(self, meal: MealSchema) -> MealSchema | None:
        user_exists = await self.session.scalar(select(User).where(User.telegram_id == meal.user_id))
        if not user_exists:
            return None
        new_meal = Meal(description=meal.description, calorie_count=meal.calorie_count, carbs_count=meal.carbs_count,
                        protein_count=meal.protein_count, fats_count=meal.fats_count, user_id=meal.user_id)
        self.session.add(new_meal)
        await self.session.commit()
        await self.session.refresh(new_meal)
        return new_meal

    async def update_meal(self, meal: MealSchema, meal_id: int) -> Any:
        upd_meal = await self.session.scalar(select(Meal).where(Meal.id == meal_id))
        if not upd_meal:
            return None
        upd_meal.description = meal.description
        upd_meal.calorie_count = meal.calorie_count
        upd_meal.carbs_count = meal.carbs_count
        upd_meal.protein_count = meal.protein_count
        upd_meal.fats_count = meal.fats_count
        await self.session.commit()
        await self.session.refresh(upd_meal)
        return MealSchema.model_validate(upd_meal)

    async def fetch_meal(self, user_id: int, timestamp: Optional[datetime]=None) -> Any:
        if timestamp == None:
            meals = await paginate(self.session,
                               select(Meal).where(Meal.user_id == user_id).order_by(
                                   Meal.timestamp.desc()))
        else:
            tstmp_low = timestamp
            tstmp_high = timestamp.replace(hour=23, minute=59, second=59)
            print(f'{tstmp_low} {tstmp_high}')
            meals = await paginate(self.session,
                               select(Meal).where(Meal.user_id == user_id).where(and_(Meal.timestamp >= tstmp_low, Meal.timestamp <= tstmp_high)).order_by(
                                   Meal.timestamp.desc()))
        return meals

    async def delete_meal(self, meal_id: int) -> bool:
        meal = await self.session.scalar(select(Meal).where(Meal.id == meal_id))
        if meal:
            await self.session.delete(meal)
            await self.session.commit()
            return True
        else:
            return False
    
    async def fetch_meal_by_id(self, meal_id: int) -> MealSchema | None:
        meal = await self.session.scalar(select(Meal).where(Meal.id == meal_id))
        if not meal:
            return None
        return meal
        
async def get_meal_manager(db: AsyncSession = Depends(get_db)) -> MealRequestManager:
    return MealRequestManager(db)