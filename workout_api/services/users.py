from typing import List, Optional

from sqlalchemy.orm import Session
from fastapi import Depends

from .. import tables
from ..database import get_session
from .. import models


class UsersService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_users(self, user_type: Optional[models.UserType] = None) -> List[tables.User]:
        query = self.session.query(tables.User)
        if user_type:
            query = query.filter_by(user_type=user_type)
        users = query.all()
        return users

    def create_user(self, user_data: models.UserCreate) -> tables.User:
        user = tables.User(**user_data.dict())
        self.session.add(user)
        self.session.commit()
        return user
