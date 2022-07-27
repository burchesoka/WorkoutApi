from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class BasePayment(BaseModel):
    sum: int
    workouts_left: int
    datetime: datetime
    user_telegram_id: int
    group_id: int
    verified: bool
    comment: Optional[str]


class PaymentCreate(BasePayment):
    pass


class PaymentUpdate(BasePayment):
    pass


class Payment(BasePayment):
    id: int

    class Config:
        orm_mode = True
