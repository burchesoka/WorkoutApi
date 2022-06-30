from typing import List, Optional

from fastapi import (
    APIRouter,
    Depends,
    Response,
    status,
)

from .. import models
from ..services.users import UsersService


router = APIRouter(
    prefix='/users',
    tags=['users'],
)


@router.get(
    '/',
    response_model=List[models.User],
)
async def get_users(
    user_status: Optional[models.UserStatus] = None,
):
    service = UsersService()
    return await service.get_many(user_status=user_status)


@router.get('/{user_id}', response_model=models.User,)
async def get_user(user_id: int,):
    service = UsersService()
    return await service.get(user_id)


@router.get('/telegram/{telegram_id}', response_model=models.User)
async def get_user_by_telegram_id(telegram_id: int):
    service = UsersService()
    return await service.get_user_by_telegram_id(telegram_id)


@router.post(
    '/',
    response_model=models.User,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(user_data: models.UserCreate,):
    service = UsersService()
    return await service.create(user_data)


@router.put('/{user_id}', response_model=models.User)
async def update_user(
        user_id: int,
        user_data: models.UserUpdate
):
    service = UsersService()
    return await service.update(user_id, user_data)


@router.delete('/{user_id}')
async def delete_user(user_id: int):
    service = UsersService()
    await service.delete(user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
