import logging

from typing import List

from .. import tables
from ..database import database
from .. import models
from .base_service import BaseService


logger = logging.getLogger(__name__)


class TrainersService(BaseService):
    async def get_many(self) -> List[models.Trainer]:
        query = tables.trainer.select()
        return await database.fetch_all(query)

    async def get(self, trainer_id: int) -> tables.trainer:
        query = tables.trainer.select().where(tables.trainer.c.id == trainer_id)
        return await self._fetch_one_or_404(query)

    async def get_trainer_by_telegram_id(self, telegram_id: int) -> tables.trainer:
        query = tables.trainer.select().where(tables.trainer.c.telegram_id == telegram_id)
        return await self._fetch_one_or_404(query)

    async def create(self, trainer_data: models.TrainerCreate) -> tables.trainer:
        query = tables.trainer.insert().values(
            **trainer_data.dict()
        ).returning(tables.trainer)

        trainer = await self._fetch_one_or_404(query)
        trainer_profile_query = tables.trainer_profile.insert().values(trainer_id=trainer.id)
        await self._fetch_one_or_404(trainer_profile_query)
        trainer_stats_query = tables.trainer_stats.insert().values(trainer_id=trainer.id)
        await self._fetch_one_or_404(trainer_stats_query)
        return trainer

    async def update(self, trainer_id: int, trainer_data: models.TrainerUpdate) -> tables.trainer:
        query = (
            tables.trainer.update()
            .where(tables.trainer.c.id == trainer_id)
            .values(**trainer_data.dict())
            .returning(tables.trainer)
        )
        return await self._fetch_one_or_404(query)

    async def delete(self, trainer_id):
        query = tables.trainer_profile.delete().where(tables.trainer_profile.c.trainer_id == trainer_id)
        await database.execute(query)
        query = tables.trainer_stats.delete().where(tables.trainer_stats.c.trainer_id == trainer_id)
        await database.execute(query)
        query = tables.trainer.delete().where(tables.trainer.c.id == trainer_id)
        await database.execute(query)
