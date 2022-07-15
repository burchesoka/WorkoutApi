from typing import List

from fastapi import (
    APIRouter,
    Response,
    status,
)

from .. import models
from ..services.groups import GroupsService


router = APIRouter(
    prefix='/groups',
    tags=['groups'],
)

service = GroupsService()


@router.get(
    '/',
    response_model=List[models.Group],
)
async def get_groups():
    return await service.get_many()


@router.get('/{group_id}', response_model=models.Group,)
async def get_group(group_id: int,):
    return await service.get(group_id)


@router.get('/by_trainer/{trainer_telegram_id}', response_model=List[models.Group])
async def get_groups_by_trainer_telegram_id(trainer_telegram_id: int):
    return await service.get_groups_by_trainer_telegram_id(trainer_telegram_id)


@router.post(
    '/',
    response_model=models.Group,
    status_code=status.HTTP_201_CREATED,
)
async def create_group(group_data: models.GroupCreate,):
    return await service.create(group_data)


@router.post(
    '/add_user_to_group',
    response_model=models.UserGroup,
    status_code=status.HTTP_201_CREATED,
)
async def add_user_to_group(data: models.AddUserToGroup,):
    return await service.add_user_to_group(data)


@router.put('/{group_id}', response_model=models.Group)
async def update_group(
        group_id: int,
        group_data: models.GroupUpdate
):
    return await service.update(group_id, group_data)


@router.delete('/{group_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_group(group_id: int):
    await service.delete(group_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
