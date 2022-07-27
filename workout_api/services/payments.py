import logging

from typing import List

from .. import tables
from ..database import database
from .. import models
from .base_service import BaseService
from .nats import send_message_to_bot
from .users import UsersService


logger = logging.getLogger(__name__)


class PaymentsService(BaseService):
    async def get_many(self, query=None) -> List[models.Payment]:
        if query is None:
            query = tables.payment.select()
        return await database.fetch_all(query)

    async def get(self, payment_id: int) -> tables.payment:
        query = tables.payment.select().where(tables.payment.c.id == payment_id)
        return await self._fetch_one_or_404(query)

    async def get_payments_by_user_id(self, user_id: int) -> List[models.Payment]:
        query = tables.payment.select().where(tables.payment.c.user_id == user_id)
        return await self.get_many(query=query)

    async def create(self, group_data: models.PaymentCreate) -> tables.payment:
        query = tables.payment.insert().values(
            **group_data.dict()
        ).returning(tables.payment)
        return await self._fetch_one_or_404(query)

    async def update(self, payment_id: int, payment_data: models.PaymentUpdate) -> tables.payment:
        query = (
            tables.payment.update()
            .where(tables.payment.c.id == payment_id)
            .values(**payment_data.dict())
            .returning(tables.payment)
        )
        return await self._fetch_one_or_404(query)

    async def confirm(self, payment_id: int) -> tables.payment:
        payment = await self.get(payment_id)

        query = (
            tables.payment.update()
            .where(tables.payment.c.id == payment_id)
            .values(
                sum=payment.sum,
                workouts_left=payment.workouts_left,
                datetime=payment.datetime,
                user_telegram_id=payment.user_telegram_id,
                group_id=payment.group_id,
                verified=True
            )
            .returning(tables.payment)
        )
        updated_payment = await self._fetch_one_or_404(query)
        users_service = UsersService()
        user = await users_service.get_user_by_telegram_id(telegram_id=payment.user_telegram_id)
        await send_message_to_bot(
            user_telegram_id=user.telegram_id,
            message=f'Платеж на сумму {payment.sum} подтвержден! Спасибо!'
        )
        logger.info(f'Payment (id {payment_id}) confirmed')
        return updated_payment

    async def reject(self, payment_id: int):
        payment = await self.get(payment_id)
        await self.delete(payment_id)

        users_service = UsersService()
        user = await users_service.get_user_by_telegram_id(telegram_id=payment.user_telegram_id)

        await send_message_to_bot(user_telegram_id=user.telegram_id,
                                  message=f'Платеж на сумму {payment.sum} отклонен.\n'
                                          f'Пожалуйста, проверьте всё и отметьте платёж снова\n'
                                          f'/pay')
        logger.info(f'Payment (id {payment_id}) rejecnted and deleted')

    async def delete(self, payment_id: int):
        query = tables.payment.delete().where(tables.payment.c.id == payment_id)
        await database.execute(query)
