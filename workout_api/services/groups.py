import logging
import asyncpg
from typing import List


from fastapi import status, HTTPException

from .. import tables
from ..database import database
from .. import models
from .users import UsersService


logger = logging.getLogger(__name__)


class GroupsService:
    async def _fetch_one_or_404(self, query) -> object:
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
        if query is None:
            query = tables.group.select()
        return await database.fetch_all(query)

    async def get(self, group_id: int) -> tables.group:
        query = tables.group.select().where(tables.group.c.id == group_id)
        return await self._fetch_one_or_404(query)

    async def get_groups_by_trainer_telegram_id(self, trainer_telegram_id: int) -> List[models.Group]:
        query = tables.group.select().where(tables.group.c.trainer_telegram_id == trainer_telegram_id)
        return await self.get_many(query=query)

    async def create(self, group_data: models.GroupCreate) -> tables.group:
        query = tables.group.insert().values(
            **group_data.dict()
        ).returning(tables.group)

        return await self._fetch_one_or_404(query)

    async def add_user_to_group(self, data: models.AddUserToGroup) -> tables.users_groups:
        """
        Добавляет пользователя в группу, если пользователя с таким телефоном нет,
        то создает его и добавляет в группу заготовку пользователя
        """
        data_dict = data.dict()
        user_phone = data_dict.pop('user_phone')
        user_services = UsersService()

        try:
            user = await user_services.get_user_by_phone(user_phone)
        except HTTPException as e:
            logger.info('User not found - creating!' + str(e))
            user = None

        if not user:
            user_data = models.UserCreate(
                name=data.user_name_for_trainer,
                phone=data.user_phone,
                status=models.UserStatus.just_added_by_trainer
            )
            user = await user_services.create(user_data)

        data_dict['user_id'] = user.id

        query = tables.users_groups.insert().values(
            **data_dict
        ).returning(tables.users_groups)

        return await self._fetch_one_or_404(query)

    async def update(self, group_id: int, group_data: models.GroupUpdate) -> tables.group:
        query = (
            tables.group.update()
            .where(tables.group.c.id == group_id)
            .values(**group_data.dict())
            .returning(tables.group)
        )
        return await self._fetch_one_or_404(query)

    async def delete(self, group_id):
        query = tables.group.delete().where(tables.group.c.id == group_id)
        await database.execute(query)
