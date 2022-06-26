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

    def create_user(self, user_data: models.UserCreate) -> tables.User:
        user = tables.User(**user_data.dict())
        self.session.add(user)
        try:
            self.session.commit()
        except IntegrityError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e}')
        return user
