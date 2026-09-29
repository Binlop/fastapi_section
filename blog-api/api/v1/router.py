from fastapi import APIRouter

router = APIRouter(prefix="/api/v1")

from api.v1.users import router as user_router

router.include_router(user_router)