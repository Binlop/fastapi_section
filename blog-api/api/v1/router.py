from fastapi import APIRouter

router = APIRouter(prefix="/api/v1")

from api.v1.auth import router as auth_router
from api.v1.posts import router as posts_router

router.include_router(auth_router)
router.include_router(posts_router)