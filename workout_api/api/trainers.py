from typing import List

from fastapi import (
    APIRouter,
    Response,
    status,
)

from .. import models
from ..services.trainers import TrainersService


router = APIRouter(
    prefix='/trainers',
    tags=['trainers'],
)

service = TrainersService()


@router.get(
    '/',
    response_model=List[models.Trainer],
)
async def get_trainers():
    return await service.get_many()


@router.get('/{trainer_id}', response_model=models.Trainer,)
async def get_trainer(trainer_id: int,):
    return await service.get(trainer_id)


@router.get('/telegram/{telegram_id}', response_model=models.Trainer)
async def get_trainer_by_telegram_id(telegram_id: int):
    return await service.get_trainer_by_telegram_id(telegram_id)


@router.post(
    '/',
    response_model=models.Trainer,
    status_code=status.HTTP_201_CREATED,
)
async def create_trainer(trainer_data: models.TrainerCreate,):
    return await service.create(trainer_data)


@router.put('/{trainer_id}', response_model=models.Trainer)
async def update_trainer(
        trainer_id: int,
        trainer_data: models.TrainerUpdate
):
    return await service.update(trainer_id, trainer_data)


@router.delete('/{trainer_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_trainer(trainer_id: int):
    await service.delete(trainer_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
