import logging
from typing import List, Optional

from fastapi import (
    APIRouter,
    Depends,
    Response,
    status,
)

from .. import tables
from .. import models
from ..services.users import UsersService


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix='/users',
    tags=['users'],
)

service = UsersService()


@router.get('/', response_model=List[models.User])
async def get_users(
    user_status: Optional[models.UserStatus] = None,
    services: UsersService = Depends()
):
    logger.debug('get_users')
    return await services.get_many(
        table=tables.User,
        wanted=user_status,
        column=tables.User.status,
    )


@router.get('/{user_id}', response_model=models.User)
async def get_user(user_id: int,
                   services: UsersService = Depends()):
    logger.info('get_user by id: ' + str(user_id))
    user = await services.get_or_404(
        table=tables.User,
        wanted=user_id
    )
    return user


@router.get('/telegram/{telegram_id}', response_model=models.User)
async def get_user_by_telegram_id(telegram_id: int,
                                  services: UsersService = Depends()):
    logger.info('get_user_by_telegram_id: ' + str(telegram_id))

    return await services.get_or_404(
        table=tables.User,
        wanted=telegram_id,
        column=tables.User.telegram_id,
    )


@router.get('/phone/{phone}', response_model=models.User)
async def get_user_by_phone(phone: int,
                            services: UsersService = Depends()):
    logger.info('get_user_by_phone' + str(phone))
    user = await services.get_or_404(
        wanted=phone,
        table=tables.User,
        column=tables.User.phone,
    )
    return user


@router.post(
    '/',
    response_model=models.User,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(user_data: models.UserCreate,
                      services: UsersService = Depends()):
    logger.info('create_user' + str(user_data))
    return await services.create_user_profile_stats(user_data)


@router.put('/{user_id}', response_model=models.User)
async def update_user(
        user_id: int,
        user_data: models.UserUpdate,
        services: UsersService = Depends()
):
    logger.info('update_user id:' + str(user_id) + ' data: ' + str(user_data))
    return await services.update(
        table=tables.User,
        wanted=user_id,
        data=user_data.dict(),
        column=tables.User.id
    )


@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int,
                      services: UsersService = Depends()):
    await services.delete_user(user_id)
    logger.info('deleted_user id: ' + str(user_id))
    return Response(status_code=status.HTTP_204_NO_CONTENT)
