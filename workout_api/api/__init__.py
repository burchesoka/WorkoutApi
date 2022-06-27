from fastapi import APIRouter

from . import (
    users,
    not_registered_users,
)

router = APIRouter()
router.include_router(users.router)
router.include_router(not_registered_users.router)
