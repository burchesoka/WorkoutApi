from fastapi import APIRouter

from . import (
    users,
    trainers,
)

router = APIRouter()
router.include_router(users.router)
router.include_router(trainers.router)
