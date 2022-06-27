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
def get_users(
    user_status: Optional[models.UserStatus] = None,
    users_service: UsersService = Depends(),
):
    return users_service.get_users(user_status=user_status)


@router.get('/{user_id}', response_model=models.User,)
def get_user(
    user_id: int,
    users_service: UsersService = Depends(),
):
    return users_service.get(user_id)


@router.get('/telegram/{telegram_id}', response_model=models.User)
def get_user_by_telegram_id(
        telegram_id: int,
        user_service: UsersService = Depends()
):
    return user_service.get_user_by_telegram_id(telegram_id)


@router.post(
    '/',
    response_model=models.User,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    user_data: models.UserCreate,
    users_service: UsersService = Depends(),

):
    return users_service.create(user_data)


@router.put('/{user_id}', response_model=models.User)
def update_user(
        user_id: int,
        user_data: models.UserUpdate,
        users_service: UsersService = Depends()
):
    return users_service.update(user_id, user_data)


@router.delete('/{user_id}')
def delete_user(
    user_id: int,
    users_service: UsersService = Depends(),

):
    users_service.delete(user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
