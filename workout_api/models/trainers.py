from typing import Optional

from pydantic import BaseModel


class BaseTrainer(BaseModel):
    name: str
    phone: int  # как задать количество символов в номере?
    telegram_id: Optional[int]


class TrainerCreate(BaseTrainer):
    pass


class TrainerUpdate(BaseTrainer):
    pass


class Trainer(BaseTrainer):
    id: int

    class Config:
        orm_mode = True
