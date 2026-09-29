from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=['Users'])

class UserViews:
    """Эндпоинты для работы с пользователями."""
    
    @router.get("/")
    async def get_users():
        return [{"id": 1, "username": "admin"}]

    @router.post("/")
    async def create_user():
        return {"message": "Пользователь создан"}

    @router.get("/{user_id}")
    async def get_user(user_id: int):
        return {"id": user_id, "username": "admin"}

    @router.delete("/{user_id}")
    async def delete_user(user_id: int):
        return {"message": "Пользователь удалён"}