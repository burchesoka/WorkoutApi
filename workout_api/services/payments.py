import logging
import asyncpg
from typing import List


from fastapi import status, HTTPException

from .. import tables
from ..database import database
from .. import models


logger = logging.getLogger(__name__)


class PaymentsService:
    async def _fetch_one_or_404(self, query) -> object:
        try:
            payment = await database.fetch_one(query)
        except asyncpg.exceptions.UniqueViolationError as e:
            logger.info(e)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e}')
        except asyncpg.exceptions.DataError as e:
            logger.info(e)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e}')

        if not payment:
            logger.warning('payment not found')
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return payment

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

    async def update(self, payment_id: int, group_data: models.PaymentUpdate) -> tables.payment:
        query = (
            tables.payment.update()
            .where(tables.payment.c.id == payment_id)
            .values(**group_data.dict())
            .returning(tables.payment)
        )
        return await self._fetch_one_or_404(query)

    async def delete(self, payment_id):
        query = tables.payment.delete().where(tables.payment.c.id == payment_id)
        await database.execute(query)
