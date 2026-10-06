from fastapi import APIRouter, Request, Depends
from auth.service import create_user, login_user
from auth.schemas import UserRegister
from api.deps import get_current_user, User

router = APIRouter(prefix="/auth", tags=['Auth'])

class UserViews:
    """Эндпоинты для работы с пользователями."""
    
    @router.get("/")
    async def get_users():
        return [{"id": 1, "username": "admin"}]

    @router.post("/register", status_code=201)
    async def create_user(data: UserRegister):
        return await create_user(data)
    
    @router.post("/login",  status_code=200)
    async def login_user(data: UserRegister):
        return await login_user(data)

    @router.get("/profile")
    async def get_user(user: User = Depends(get_current_user)):
        return {"message": 'ok', 'email': user['email']}

    @router.delete("/{user_id}")
    async def delete_user(user_id: int):
        return {"message": "Пользователь удалён"}