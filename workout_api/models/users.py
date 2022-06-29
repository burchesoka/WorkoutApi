from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class UserStatus(str, Enum):
    user = "user"
    user_without_trainer = "user_without_trainer"
    new_user = "new"


class UserGender(str, Enum):
    male = "male"
    female = "female"


class BaseUser(BaseModel):
    name: str
    phone: int  # как задать количество символов в номере?
    status: UserStatus
    telegram_id: Optional[int]


class UserCreate(BaseUser):
    pass


class UserUpdate(BaseUser):
    pass


class User(BaseUser):
    id: int

    class Config:
        orm_mode = True


class BaseProfile(BaseModel):
    user_id: int
    city: Optional[str]
    gender: Optional[UserGender]
    age: Optional[int]


class ProfileCreate(BaseProfile):
    pass


class ProfileUpdate(BaseProfile):
    pass


class Profile(BaseProfile):
    id: int
    date_created: datetime
    date_updated: datetime

    class Config:
        orm_mode = True


class BaseUserStats(BaseModel):
    user_id: int
    visited_events: Optional[int]
    skipped_events: Optional[int]


class UserStatsCreate(BaseUserStats):
    pass


class UserStatsUpdate(BaseUserStats):
    pass


class UserStats(BaseUserStats):
    id: int

    class Config:
        orm_mode = True
