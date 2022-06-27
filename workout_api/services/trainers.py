from typing import List, Optional

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import Depends, status, HTTPException

from .. import tables
from ..database import get_session
from .. import models


class TrainersService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_many(self) -> List[tables.Trainer]:
        query = self.session.query(tables.Trainer)
        trainers = query.all()
        return trainers

    def _get(self, trainer_id):
        trainer = (
            self.session
            .query(tables.Trainer)
            .filter_by(id=trainer_id)
            .first()
        )
        if not trainer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return trainer

    def get(self, trainer_id: int) -> tables.Trainer:
        return self._get(trainer_id)

    def get_user_by_telegram_id(self, telegram_id: int) -> tables.Trainer:
        trainer = (
            self.session
            .query(tables.Trainer)
            .filter_by(telegram_id=telegram_id)
            .first()
        )
        if not trainer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return trainer

    def create(self, trainer_data: models.TrainerCreate) -> tables.Trainer:
        user = tables.User(**trainer_data.dict())
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