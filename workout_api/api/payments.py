from typing import List

from fastapi import (
    APIRouter,
    Response,
    status,
)

from .. import models
from ..services.payments import PaymentsService


router = APIRouter(
    prefix='/payments',
    tags=['payments'],
)

service = PaymentsService()


@router.get(
    '/',
    response_model=List[models.Payment],
)
async def get_payments():
    return await service.get_many()


@router.get('/{payment_id}', response_model=models.Payment,)
async def get_payment(group_id: int,):
    return await service.get(group_id)


@router.get('/by_user/{user_id}', response_model=List[models.Payment])
async def get_payments_by_user_id(trainer_telegram_id: int):
    return await service.get_payments_by_user_id(trainer_telegram_id)


@router.post(
    '/',
    response_model=models.Payment,
    status_code=status.HTTP_201_CREATED,
)
async def create_payment(payment_data: models.PaymentCreate,):
    return await service.create(payment_data)


@router.put('/{payment_id}', response_model=models.Payment)
async def update_payment(
        group_id: int,
        group_data: models.PaymentUpdate
):
    return await service.update(group_id, group_data)


@router.delete('/{payment_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_payment(payment_id: int):
    await service.delete(payment_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
