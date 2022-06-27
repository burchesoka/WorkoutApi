from typing import List, Optional

from fastapi import (
    APIRouter,
    Depends,
    Response,
    status,
)

from .. import models
from ..services.trainers import TrainersService


router = APIRouter(
    prefix='/trainers',
    tags=['trainers'],
)


@router.get(
    '/',
    response_model=List[models.Trainer],
)
def get_trainers(
    trainers_service: TrainersService = Depends(),
):
    return trainers_service.get_many()


@router.get('/{user_id}', response_model=models.Trainer,)
def get_user(
    user_id: int,
    trainers_service: TrainersService = Depends(),
):
    return trainers_service.get(user_id)


@router.get('/telegram/{telegram_id}', response_model=models.Trainer)
def get_user_by_telegram_id(
        telegram_id: int,
        trainers_service: TrainersService = Depends()
):
    return trainers_service.get_user_by_telegram_id(telegram_id)


@router.post(
    '/',
    response_model=models.User,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    trainer_data: models.TrainerCreate,
    trainers_service: TrainersService = Depends(),

):
    return trainers_service.create(trainer_data)


@router.put('/{user_id}', response_model=models.Trainer)
def update_user(
        user_id: int,
        user_data: models.UserUpdate,
        trainers_service: TrainersService = Depends()
):
    return trainers_service.update(user_id, user_data)


@router.delete('/{user_id}')
def delete_user(
    user_id: int,
    trainers_service: TrainersService = Depends(),

):
    trainers_service.delete(user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
