from fastapi import HTTPException, Depends, status, Response, APIRouter, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, Optional
from slowapi import Limiter
from slowapi.util import get_remote_address
import os

from app.utils.schemas import UserSchema, UserMacrosUpdateSchema
from app.database.data_managers.user_manager import UserRequestManager, get_user_manager
from app.database import get_db
from app.utils.security import get_api_key

limiter = Limiter(
    key_func = get_remote_address,
    strategy="fixed-window",
    storage_uri='memory://'
)

user_manager = Annotated[UserRequestManager, Depends(get_user_manager)]
security = Annotated[str, Depends(get_api_key)]
router = APIRouter(prefix='/api/user', tags=['Users'], dependencies=[Depends(get_api_key)])

#Get user info by id
@router.get("/{user_id}", status_code=status.HTTP_200_OK)
@limiter.limit("5/second", per_method=True)
async def get_user_by_id(manager: user_manager, user_id: int, request: Request):
    user = await manager.fetch_user(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No user with {user_id} ID.')
    else:
        return user

#Register a new user macros
@router.post("/", status_code=status.HTTP_201_CREATED)
@limiter.limit("5/second", per_method=True)
async def create_user_macros(user: UserSchema, manager: user_manager, request: Request) -> UserSchema:
    new_user, message = await manager.create_user(user)
    if not new_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=message)
    return new_user

#Update user macros
@router.put("/{user_id}", status_code=status.HTTP_200_OK)
@limiter.limit("5/second", per_method=True)
async def update_user_macros(user_id: int, user: UserSchema, manager: user_manager, request: Request) -> UserSchema:
    upd_user = await manager.update_user(user, user_id)
    if not upd_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with ID {user_id} not found.')
    return upd_user

#Delete user data
@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
@limiter.limit("5/second", per_method=True)
async def delete_user_macros(user_id: int, manager: user_manager, request: Request):
    is_deleted = await manager.delete_user(user_id)
    if not is_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with ID {user_id} not found.')
    else:
        return {'detail': f'User {user_id} successfully deleted.'}