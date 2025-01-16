from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserSchema(BaseModel):
    telegram_id: int
    full_name: str
    calorie_macros: int
    carbs_macros: float
    protein_macros: float
    fats_macros: float

class UserMacrosUpdateSchema(BaseModel):
    telegram_id: int
    calorie_macros: int
    carbs_macros: float
    protein_macros: float
    fats_macros: float

class MealSchemaReturn(BaseModel):
    id: int
    description: str
    calorie_count: int
    carbs_count: float
    protein_count: float
    fats_count: float
    user_id: int

    class Config:
        orm_mode: True

class MealSchemaInput(BaseModel):
    description: str
    calorie_count: int
    carbs_count: float
    protein_count: float
    fats_count: float
    user_id: int

class MealSchemaInput(BaseModel):
    description: str
    calorie_count: int
    carbs_count: float
    protein_count: float
    fats_count: float
    user_id: int

