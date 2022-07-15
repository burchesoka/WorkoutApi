from pydantic import BaseModel
from datetime import datetime


class BasePayment(BaseModel):
    sum: int
    workouts_left: int
    datetime: datetime
    user_id: int
    group_id: int
    verified: bool


class PaymentCreate(BasePayment):
    pass


class PaymentUpdate(BasePayment):
    pass


class Payment(BasePayment):
    id: int

    class Config:
        orm_mode = True
