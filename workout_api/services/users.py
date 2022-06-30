import asyncpg
from typing import List, Optional

from sqlalchemy.orm import Session
from fastapi import Depends, status, HTTPException

from .. import tables
from ..database import get_session, database
from .. import models


class UsersService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    async def _get_or_404(self, query) -> object:
        try:
            user = await database.fetch_one(query)
        except asyncpg.exceptions.UniqueViolationError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e}')
        except asyncpg.exceptions.DataError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e}')

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return user

    async def get_many(self, user_status: Optional[models.UserStatus] = None) -> List[tables.user]:
        if user_status:
            query = tables.user.select().where(tables.user.c.status == user_status)
            return await database.fetch_all(query)
        query = tables.user.select()
        return await database.fetch_all(query)

    async def get(self, user_id: int) -> tables.user:
        query = tables.user.select().where(tables.user.c.id == user_id)
        return await self._get_or_404(query)

    async def get_user_by_telegram_id(self, telegram_id: int) -> tables.user:
        query = tables.user.select().where(tables.user.c.telegram_id == telegram_id)
        return await self._get_or_404(query)

    async def get_user_by_phone(self, phone: int) -> tables.user:
        query = tables.user.select().where(tables.user.c.phone == phone)
        return await self._get_or_404(query)

    async def create(self, user_data: models.UserCreate) -> tables.user:
        # TODO Добваить статс и профиль

        # user = tables.User(**user_data.dict())
        # self.session.add(user)
        # self._commit(self.session)
        #
        # user_profile = models.ProfileCreate(user_id=user.id)
        # self.session.add(tables.Profile(**user_profile.dict()))
        # self._commit(self.session)
        #
        # user_stats = models.UserStatsCreate(user_id=user.id)
        # self.session.add(tables.UserStats(**user_stats.dict()))
        # self._commit(self.session)

        query = tables.user.insert().values(**user_data.dict()).returning(
            tables.user.c.id,
            tables.user.c.name,
            tables.user.c.phone,
            tables.user.c.status,
            tables.user.c.telegram_id,
        )
        return await self._get_or_404(query)

    async def update(self, user_id: int, user_data: models.UserUpdate) -> tables.user:
        query = (
            tables.user.update()
            .where(tables.user.c.id == user_id)
            .values(**user_data.dict()).returning(
            tables.user.c.id,
            tables.user.c.name,
            tables.user.c.phone,
            tables.user.c.status,
            tables.user.c.telegram_id,
        )
        )
        return await self._get_or_404(query)

    async def delete(self, user_id):
        # TODO Удалить сначала статс и профиль
        query = tables.user.delete().where(tables.user.c.id == user_id)
        await database.execute(query)
