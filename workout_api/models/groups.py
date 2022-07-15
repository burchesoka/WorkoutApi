from pydantic import BaseModel


class BaseGroup(BaseModel):
    title: str
    trainer_telegram_id: int


class GroupCreate(BaseGroup):
    pass


class GroupUpdate(BaseGroup):
    pass


class Group(BaseGroup):
    id: int

    class Config:
        orm_mode = True


class BaseUserGroup(BaseModel):
    group_id: int
    user_name_for_trainer: str


class AddUserToGroup(BaseUserGroup):
    user_phone: int


class UserGroup(BaseUserGroup):
    user_id: int

    class Config:
        orm_mode = True
