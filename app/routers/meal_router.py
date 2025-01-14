from fastapi import HTTPException, Depends, status, Response, APIRouter, Query, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, Optional
import os
from fastapi_pagination import Page, LimitOffsetPage
from datetime import datetime
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.utils.security import get_api_key
from app.utils.schemas import MealSchemaInput, MealSchemaReturn
from app.database.data_managers.meal_manager import MealRequestManager, get_meal_manager
from app.database import get_db

manager = Annotated[MealRequestManager, Depends(get_meal_manager)]
router = APIRouter(prefix='/api/meal', tags=['Meals'], dependencies=[Depends(get_api_key)])
limiter = Limiter(
    key_func = get_remote_address,
    strategy="fixed-window",
    storage_uri='memory://'
)

#Add a meal
@router.post("/", status_code=status.HTTP_201_CREATED)
@limiter.limit("5/second", per_method=True)
async def add_meal(meal: MealSchemaInput, manager: manager, request: Request) -> MealSchemaReturn:
    new_meal = await manager.create_meal(meal)
    if not new_meal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with telegram ID {meal.user_id} does not exist')
    return new_meal

#Retrieve a set number of meals (limited)
#@router.get("/limit-offset", status_code=status.HTTP_200_OK, response_model=LimitOffsetPage[MealSchema])
@router.get("/", status_code=status.HTTP_200_OK, response_model=Page[MealSchemaReturn])
@limiter.limit("5/second", per_method=True)
async def get_meal(manager: manager, user_id: int, request: Request, timestamp: Optional[datetime]=None):
    meals = await manager.fetch_meal(user_id, timestamp)    
    if not meals:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No meals found')
    return meals

#Retrieve a meal by id
@router.get("/{meal_id}", status_code=status.HTTP_200_OK)
@limiter.limit("5/second", per_method=True)
async def get_meal_by_id(manager: manager, meal_id: int, request: Request) -> MealSchemaReturn:
    meal = await manager.fetch_meal_by_id(meal_id)
    if not meal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No meals with ID {meal_id} found')
    return meal

#Update meal data
@router.put("/{meal_id}", status_code=status.HTTP_200_OK)
@limiter.limit("5/second", per_method=True)
async def update_meal(meal_id: int, meal: MealSchemaReturn, manager: manager, request: Request):
    meal = await manager.update_meal(meal, meal_id)
    if not meal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No meals with ID {meal_id} found')
    return meal

#Delete meal data
@router.delete("/{meal_id}", status_code=status.HTTP_200_OK)
@limiter.limit("5/second", per_method=True)
async def delete_meal(meal_id: int, manager: manager, request: Request):
    result = await manager.delete_meal(meal_id)
    if result:
        return {'detail': f"Meal with ID {meal_id} was deleted successfully."}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No meals with ID {meal_id} found')
