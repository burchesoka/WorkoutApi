import logging
import asyncpg
from typing import List


from fastapi import status, HTTPException

from .. import tables
from ..database import database
from .. import models


logger = logging.getLogger(__name__)


class GroupsService:
    async def _get_or_404(self, query) -> object:
        try:
            group = await database.fetch_one(query)
        except asyncpg.exceptions.UniqueViolationError as e:
            logger.info(e)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e}')
        except asyncpg.exceptions.DataError as e:
            logger.info(e)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e}')

        if not group:
            logger.warning('group not found')
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return group

    async def get_many(self, query=None) -> List[models.Group]:
        if query == None:
            query = tables.group.select()
        return await database.fetch_all(query)

    async def get(self, group_id: int) -> tables.group:
        query = tables.group.select().where(tables.group.c.id == group_id)
        return await self._get_or_404(query)

    async def get_groups_by_trainer_telegram_id(self, trainer_telegram_id: int) -> List[models.Group]:
        query = tables.group.select().where(tables.group.c.trainer_telegram_id == trainer_telegram_id)
        return await self.get_many(query=query)

    async def create(self, group_data: models.GroupCreate) -> tables.group:
        query = tables.group.insert().values(
            **group_data.dict()
        ).returning(tables.group)

        group = await self._get_or_404(query)
        return group

    async def update(self, group_id: int, trainer_data: models.GroupUpdate) -> tables.group:
        query = (
            tables.group.update()
            .where(tables.group.c.id == group_id)
            .values(**trainer_data.dict())
            .returning(tables.group)
        )
        return await self._get_or_404(query)

    async def delete(self, group_id):
        query = tables.group.delete().where(tables.group.c.id == group_id)
        await database.execute(query)
