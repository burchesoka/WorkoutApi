import logging

from .. import tables
from .. import models
from .base_service import BaseService

logger = logging.getLogger(__name__)


class UsersService(BaseService):

    async def get(self, user_id: int) -> tables.User:
        return await self.get_or_404(wanted=user_id, table=tables.User)

    async def create_user_profile_stats(self, user_data: models.UserCreate) -> tables.User:
        user = await self.create(table=tables.User,
                                 data=user_data.dict())

        await self.create(table=tables.UserProfile, data={'user_id': user.id})
        await self.create(table=tables.UserStats, data={'user_id': user.id})
        return user

    async def delete_user(self, user_id):
        await self.delete(
            table=tables.UserProfile,
            entity_id=user_id,
            column=tables.UserProfile.user_id
        )
        await self.delete(
            table=tables.UserStats,
            entity_id=user_id,
            column=tables.UserStats.user_id
        )
        await self.delete(
            table=tables.User,
            entity_id=user_id
        )
