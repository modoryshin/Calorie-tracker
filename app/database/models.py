from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship, WriteOnlyMapped
from sqlalchemy import BigInteger, String, DateTime, Integer, Float, ForeignKey
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.sql import func
from datetime import datetime, timezone
from typing import Optional

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger)
    full_name: Mapped[str] = mapped_column(String(30))
    calorie_macros: Mapped[int] = mapped_column(Integer)
    carbs_macros: Mapped[float] = mapped_column(Float)
    protein_macros: Mapped[float] = mapped_column(Float)
    fats_macros: Mapped[float] = mapped_column(Float)
    create_date: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    meals: WriteOnlyMapped['Meal'] = relationship(back_populates='creator', passive_deletes=True)

class Meal(Base):
    __tablename__ = 'meals'

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String(50))
    calorie_count: Mapped[int] = mapped_column(Integer)
    carbs_count: Mapped[float] = mapped_column(Float)
    protein_count: Mapped[float] = mapped_column(Float)
    fats_count: Mapped[float] = mapped_column(Float)
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id), index=True)
    timestamp: Mapped[datetime] = mapped_column(index=True, default=lambda: datetime.now(timezone.utc))

    creator: Mapped[User] = relationship(back_populates='meals')
