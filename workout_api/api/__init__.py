from fastapi import APIRouter

from . import (
    users,
    trainers,
    groups,
    payments,
)

router = APIRouter()
router.include_router(users.router)
router.include_router(trainers.router)
router.include_router(groups.router)
router.include_router(payments.router)
