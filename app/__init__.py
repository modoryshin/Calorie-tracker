from fastapi import FastAPI
from fastapi_pagination import add_pagination

from app.routers.user_router import router as user_router
from app.routers.meal_router import router as meal_router
from app.middleware.middleware import LogginMiddleware

app = FastAPI()

app.add_middleware(LogginMiddleware)

add_pagination(app)

app.include_router(user_router)
app.include_router(meal_router)