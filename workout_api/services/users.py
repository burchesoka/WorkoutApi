import logging

import asyncpg
from typing import List, Optional

from sqlalchemy.orm import Session
from fastapi import Depends, status, HTTPException

from .. import tables
from ..database import get_session, database
from .. import models


logger = logging.getLogger('app.services/users')


class UsersService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    async def _get_or_404(self, query) -> object:
        try:
            logger.debug('get_or_404')
            user = await database.fetch_one(query)
        except asyncpg.exceptions.UniqueViolationError as e:
            logger.info(e)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e}')
        except asyncpg.exceptions.DataError as e:
            logger.info(e)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e}')

        if not user:
            logger.info('user not found')
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return user

    async def get_many(self, user_status: Optional[models.UserStatus] = None) -> List[models.User]:
        if user_status:
            query = tables.user.select().where(tables.user.c.status == user_status)
            return await database.fetch_all(query)
        query = tables.user.select()
        logger.debug('get_many')
        return await database.fetch_all(query)

    async def get(self, user_id: int) -> tables.user:
        query = tables.user.select().where(tables.user.c.id == user_id)
        return await self._get_or_404(query)

    async def get_user_by_telegram_id(self, telegram_id: int) -> tables.user:
        query = tables.user.select().where(tables.user.c.telegram_id == telegram_id)
        logger.debug('get_user_by_telegram_id')
        return await self._get_or_404(query)

    async def get_user_by_phone(self, phone: int) -> tables.user:
        query = tables.user.select().where(tables.user.c.phone == phone)
        return await self._get_or_404(query)

    async def create(self, user_data: models.UserCreate) -> tables.user:
        query = tables.user.insert().values(
            **user_data.dict()
        ).returning(tables.user)

        user = await self._get_or_404(query)
        user_profile_query = tables.profile.insert().values(user_id=user.id)
        await self._get_or_404(user_profile_query)
        user_stats_query = tables.user_stats.insert().values(user_id=user.id)
        await self._get_or_404(user_stats_query)
        return user

    async def update(self, user_id: int, user_data: models.UserUpdate) -> tables.user:
        query = (
            tables.user.update()
            .where(tables.user.c.id == user_id)
            .values(**user_data.dict())
            .returning(tables.user)
        )
        return await self._get_or_404(query)

    async def delete(self, user_id):
        query = tables.profile.delete().where(tables.profile.c.user_id == user_id)
        await database.execute(query)
        query = tables.user_stats.delete().where(tables.user_stats.c.user_id == user_id)
        await database.execute(query)
        query = tables.user.delete().where(tables.user.c.id == user_id)
        await database.execute(query)
