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


@router.get(
    '/',
    response_model=List[models.Group],
)
async def get_groups():
    service = GroupsService()
    return await service.get_many()


@router.get('/{group_id}', response_model=models.Group,)
async def get_group(group_id: int,):
    service = GroupsService()
    return await service.get(group_id)


@router.get('/trainers_groups/{trainer_telegram_id}', response_model=List[models.Group])
async def get_groups_by_trainer_telegram_id(trainer_telegram_id: int):
    service = GroupsService()
    return await service.get_groups_by_trainer_telegram_id(trainer_telegram_id)


@router.post(
    '/',
    response_model=models.Group,
    status_code=status.HTTP_201_CREATED,
)
async def create_group(group_data: models.GroupCreate,):
    service = GroupsService()
    return await service.create(group_data)


@router.put('/{group_id}', response_model=models.Group)
async def update_trainer(
        trainer_id: int,
        trainer_data: models.TrainerUpdate
):
    service = GroupsService()
    return await service.update(trainer_id, trainer_data)


@router.delete('/{trainer_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_trainer(trainer_id: int):
    service = GroupsService()
    await service.delete(trainer_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
