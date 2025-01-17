from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    telegram_id: int
    calorie_macros: int
    carbs_macros: float
    protein_macros: float
    fats_macros: float

class MacrosSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    calorie_macros: int
    carbs_macros: float
    protein_macros: float
    fats_macros: float

class MealSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None
    description: str
    calorie_count: int
    carbs_count: float
    protein_count: float
    fats_count: float
    user_id: int



