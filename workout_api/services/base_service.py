import logging
import asyncpg

from fastapi import status, HTTPException

from sqlalchemy.orm import Session
from fastapi import Depends

from ..database import get_session, database


logger = logging.getLogger(__name__)


class BaseService:
    def __init__(self, session: Session = Depends(get_session)):  # Нужно ли подключаться к БД какждый раз
        self.session = session

    async def _fetch_one_or_404(self, query) -> object:
        try:
            logger.debug('fetch_one_or_404')
            entry = await database.fetch_one(query)
        except asyncpg.exceptions.UniqueViolationError as e:
            logger.info(e)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e}')
        except asyncpg.exceptions.DataError as e:
            logger.info(e)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e}')

        if not entry:
            logger.warning('entry not found')
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return entry
