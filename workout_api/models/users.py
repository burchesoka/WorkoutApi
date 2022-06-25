from datetime import date
from decimal import Decimal
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class UserType(str, Enum):
    user = "user"
    trainer = "trainer"
    user_without_trainer = "user_without_trainer"
    new_user = "new_user"


class BaseUser(BaseModel):
    user_name: str
    phone: str
    user_type: UserType


class UserCreate(BaseUser):
    pass


class UserUpdate(BaseUser):
    pass


class User(BaseUser):
    id: int

    class Config:
        orm_mode = True
