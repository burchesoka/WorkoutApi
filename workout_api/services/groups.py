import logging

from typing import List

from fastapi import HTTPException

from .. import tables
from ..database import database
from .. import models
from .users import UsersService
from .base_service import BaseService
from .nats import send_message_to_bot


logger = logging.getLogger(__name__)


class GroupsService(BaseService):
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

    async def add_user_to_group_by_phone(self, data: models.AddUserToGroup) -> tables.users_groups:
        """
        Добавляет пользователя в группу, если пользователя с таким телефоном нет,
        то создает его и добавляет в группу заготовку пользователя
        Если пользователь есть, но не был в группах, то его статус меняется на юзер
        Если пользователь уже зарегестирован в боте, то ему отправляется сообщение
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

        users_groups = await self._fetch_one_or_404(query)

        if user.status == models.UserStatus.user_without_trainer:
            user_data_dict = dict(**user)
            user_data_dict.pop('id')
            user_data_dict['status'] = models.UserStatus.user

            user_data = models.UserUpdate(**user_data_dict)
            await user_services.update(user_id=user.id, user_data=user_data)

        if user.status != models.UserStatus.just_added_by_trainer:
            group = await self.get(data.group_id)
            await send_message_to_bot(
                subject='users_bot',
                recipient_telegram_id=user.telegram_id,
                message=f'Вы добавлены в группу {group.title}'
            )

        return users_groups

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
