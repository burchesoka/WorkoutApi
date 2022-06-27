from typing import List, Optional

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import Depends, status, HTTPException

from .. import tables
from ..database import get_session
from .. import models


class NotRegisteredUsersService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_many(self) -> List[tables.NotRegisteredUser]:
        query = self.session.query(tables.NotRegisteredUser)
        users = query.all()
        return users

    def _get(self, user_id):
        user = (
            self.session
            .query(tables.NotRegisteredUser)
            .filter_by(id=user_id)
            .first()
        )
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return user

    def get(self, user_id: int) -> tables.NotRegisteredUser:
        return self._get(user_id)

    def get_user_by_phone(self, phone: int) -> tables.NotRegisteredUser:
        user = (
            self.session
            .query(tables.NotRegisteredUser)
            .filter_by(phone=phone)
            .first()
        )
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return user

    def create(self, user_data: models.NotRegisteredUserCreate) -> tables.NotRegisteredUser:
        user = tables.NotRegisteredUser(**user_data.dict())
        self.session.add(user)
        try:
            self.session.commit()
        except IntegrityError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e}')
        return user

    def update(self, user_id: int, user_data: models.NotRegisteredUserUpdate) -> tables.NotRegisteredUser:
        user = self._get(user_id)
        for field, value in user_data:
            setattr(user, field, value)
        self.session.commit()
        return user

    def delete(self, user_id):
        user = self._get(user_id)
        self.session.delete(user)
        self.session.commit()
