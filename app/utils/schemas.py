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

class MealSchema(BaseModel):
    description: str
    calorie_count: int
    carbs_count: float
    protein_count: float
    fats_count: float
    user_id: int

    class Config:
        orm_mode: True

