from typing import List, Optional

from fastapi import (
    APIRouter,
    Depends,
    Response,
    status,
)

from .. import models
from ..services.not_registered_users import NotRegisteredUsersService


router = APIRouter(
    prefix='/users/not_registered_users',
    tags=['not_registered_users'],
)


@router.get(
    '/',
    response_model=List[models.NotRegisteredUser],
)
def get_users(
    users_service: NotRegisteredUsersService = Depends(),
):
    return users_service.get_many()


@router.get('/{phone}', response_model=models.NotRegisteredUser)
def get_not_registered_user(
        phone: int,
        user_service: NotRegisteredUsersService = Depends()
):
    return user_service.get_user_by_phone(phone)


@router.post(
    '/',
    response_model=models.NotRegisteredUser,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    user_data: models.NotRegisteredUserCreate,
    users_service: NotRegisteredUsersService = Depends(),

):
    return users_service.create(user_data)


@router.put('/{user_id}', response_model=models.NotRegisteredUser)
def update_user(
        user_id: int,
        user_data: models.NotRegisteredUserUpdate,
        users_service: NotRegisteredUsersService = Depends()
):
    return users_service.update(user_id, user_data)


@router.delete('/{user_id}')
def delete_user(
    user_id: int,
    users_service: NotRegisteredUsersService = Depends(),

):
    users_service.delete(user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
