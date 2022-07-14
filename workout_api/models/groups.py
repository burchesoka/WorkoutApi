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
