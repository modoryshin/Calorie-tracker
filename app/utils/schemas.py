from pydantic import BaseModel, ConfigDict, field_validator, Field, PositiveFloat, PositiveInt
from datetime import datetime
from typing import Optional

class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    telegram_id: int = Field(description='User\'s telegram ID')
    calorie_macros: PositiveInt = Field(description='User\'s calorie macros')
    carbs_macros: PositiveFloat = Field(description='User\'s carb macros')
    protein_macros: PositiveFloat = Field(description='User\'s protein macros')
    fats_macros: PositiveFloat = Field(description='User\'s fats macros')

class MacrosSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    calorie_macros: int = Field(description='User\'s calorie macros')
    carbs_macros: float = Field(description='User\'s carb macros')
    protein_macros: float = Field(description='User\'s protein macros')
    fats_macros: float = Field(description='User\'s fats macros')

class MealSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = Field(description='Meal ID', default=None)
    description: str = Field(description='Meal description')
    calorie_count: PositiveInt = Field(description='Calorie count')
    carbs_count: PositiveFloat = Field(description='Carbs count')
    protein_count: PositiveFloat = Field(description='Protein count')
    fats_count: PositiveFloat = Field(description='Fats count')
    user_id: int = Field(description='User ID')



