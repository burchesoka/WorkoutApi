from fastapi import APIRouter

from . import (
    users,
    trainers,
    groups,
)

router = APIRouter()
router.include_router(users.router)
router.include_router(trainers.router)
router.include_router(groups.router)
