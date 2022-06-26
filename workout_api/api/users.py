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


@router.post(
    '/create',
    response_model=models.User,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    user_data: models.UserCreate,
    users_service: UsersService = Depends(),

):
    return users_service.create_user(user_data)
