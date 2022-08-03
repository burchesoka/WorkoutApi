import logging
import asyncpg

from fastapi import status, HTTPException

from typing import List, Optional
from sqlalchemy import delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import Depends

from ..database import get_session, database
from .. import tables


logger = logging.getLogger(__name__)


class BaseService:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    async def _fetch_one_or_404(self, query) -> object:
        try:
            logger.debug(f'fetch_one_or_404')
            entry = await database.fetch_one(query)
        except asyncpg.exceptions.UniqueViolationError as e:
            logger.info(e)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e}')
        except asyncpg.exceptions.DataError as e:
            logger.info(e)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e}')

        if not entry:
            logger.warning('entry not found' + str(query))
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return entry

    async def get_or_404(self, table: tables.Base, wanted, column=None) -> object:
        logger.debug('get_or_404')
        if column:
            result = await self.session.execute(select(table)
                                                .where(column == wanted))
            entry = result.scalar()
        else:
            result = await self.session.get(entity=table, ident=wanted)
            entry = result

        if not entry:
            logger.warning(f'entry not found: {wanted}, table: {table}, column: {column}')
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        print(entry)
        print('id', entry.id)
        return entry

    async def get_many(self, table: tables.Base, wanted=None, column=None) -> List[object]:
        if wanted:
            result = await self.session.execute(select(table)
                                                .filter(column == wanted))
        else:
            result = await self.session.execute(select(table))
        entities = result.scalars().all()
        return entities

    async def create(self, table: tables.Base, data: dict) -> object:
        entity = table(**data)
        self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)
        return entity

    async def update(self, table: tables.Base, data: dict, wanted, column) -> object:
        update_query = update(table).where(column == wanted)\
            .values(**data).returning(table)
        select_query = select(table)\
            .from_statement(update_query)\
            .execution_options(synchronize_session='fetch')  # WTF

        entity = await self.session.scalar(select_query)
        await self.session.commit()
        await self.session.refresh(entity)
        return entity

    async def delete(self, table: tables.Base, entity_id, column=None):
        if column:
            await self.session.execute(
                delete(table).where(column == entity_id)
            )
        else:
            await self.session.execute(
                delete(table).where(table.id == entity_id)
            )
        await self.session.commit()
