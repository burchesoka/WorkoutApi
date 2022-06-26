from datetime import date
from decimal import Decimal
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class UserStatus(str, Enum):
    user = "user"
    user_without_trainer = "user_without_trainer"
    new_user = "new"


class BaseUser(BaseModel):
    name: str
    phone: int  # как задать количество символов в номере?
    status: UserStatus


class UserCreate(BaseUser):
    pass


class UserUpdate(BaseUser):
    pass


class User(BaseUser):
    id: int

    class Config:
        orm_mode = True
