from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination.ext.sqlalchemy import paginate
from typing import Optional, List, Any
from datetime import datetime
from fastapi import Depends
from fastapi_pagination import LimitOffsetPage, Page
from fastapi_pagination.ext.sqlalchemy import paginate

from app.database.models import Meal
from app.database import get_db
from app.utils.schemas import MealSchema

#Manages crud operations for user object
class MealRequestManager():
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_meal(self, meal: MealSchema) -> MealSchema:
        new_meal = Meal(description=meal.description, calorie_count=meal.calorie_count, carbs_count=meal.carbs_count,
                        protein_count=meal.protein_count, fats_count=meal.fats_count, user_id=meal.user_id)
        self.session.add(new_meal)
        await self.session.commit()
        return meal

    async def update_meal(self, meal: MealSchema, meal_id: int) -> MealSchema | None:
        upd_meal = await self.session.scalar(select(Meal).where(Meal.id == meal_id))
        if not upd_meal:
            return None
        upd_meal.calorie_count = meal.calorie_count
        upd_meal.carbs_count = meal.carbs_count
        upd_meal.protein_count = meal.protein_count
        upd_meal.fats_count = meal.fats_count
        await self.session.commit()
        return meal

    async def fetch_meal(self, user_id: int, timestamp: Optional[datetime]=None) -> Any:
        if not timestamp:
            meals = await paginate(self.session,
                               select(Meal).where(Meal.user_id == user_id).order_by(
                                   Meal.timestamp.desc()))
        else:
            meals = await paginate(self.session,
                               select(Meal).where(Meal.user_id == user_id
                                                   and Meal.timestamp == timestamp).order_by(
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
        
async def get_meal_manager(db: AsyncSession = Depends(get_db)) -> MealRequestManager:
    return MealRequestManager(db)