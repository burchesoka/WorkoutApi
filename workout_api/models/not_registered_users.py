from pydantic import BaseModel
from typing import Optional


class BaseNotRegisteredUser(BaseModel):
    name: str
    phone: int
    group_id: Optional[int]


class NotRegisteredUserCreate(BaseNotRegisteredUser):
    pass


class NotRegisteredUserUpdate(BaseNotRegisteredUser):
    pass


class NotRegisteredUser(BaseNotRegisteredUser):
    id: int

    class Config:
        orm_mode = True
