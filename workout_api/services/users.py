from typing import List, Optional

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import Depends, status, HTTPException

from .. import tables
from ..database import get_session
from .. import models


class UsersService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_users(self, user_status: Optional[models.UserStatus] = None) -> List[tables.User]:
        query = self.session.query(tables.User)
        if user_status:
            query = query.filter_by(status=user_status)
        users = query.all()
        return users

    def _get(self, user_id):
        user = (
            self.session
            .query(tables.User)
            .filter_by(id=user_id)
            .first()
        )
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return user

    def get(self, user_id: int) -> tables.User:
        return self._get(user_id)

    def get_user_by_telegram_id(self, telegram_id: int) -> tables.User:
        user = (
            self.session
            .query(tables.User)
            .filter_by(telegram_id=telegram_id)
            .first()
        )
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return user

    def create(self, user_data: models.UserCreate) -> tables.User:
        user = tables.User(**user_data.dict())
        self.session.add(user)
        try:
            self.session.commit()
        except IntegrityError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e}')
        return user

    def update(self, user_id: int, user_data: models.UserUpdate) -> tables.User:
        user = self._get(user_id)
        for field, value in user_data:
            setattr(user, field, value)
        self.session.commit()
        return user

    def delete(self, user_id):
        user = self._get(user_id)
        self.session.delete(user)
        self.session.commit()