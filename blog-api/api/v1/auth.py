from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from auth.schemas import UserCreate, UserRead, LoginRequest, TokenResponse, UserRead
from auth.domain import RegisterUserCommand, LoginUserCommand
from api.deps import UserServiceDep, UserDep

router = APIRouter(prefix="/auth", tags=['Auth'])

class UserViews:
    """Эндпоинты для работы с пользователями."""
    
    @router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
    async def register(data: UserCreate, service: UserServiceDep):
        cmd = RegisterUserCommand(email=data.email, username=data.username, password=data.password)
        return await service.register(cmd)
    
    @router.post("/login",  response_model=TokenResponse, status_code=status.HTTP_200_OK)
    async def login_json(data: LoginRequest, service: UserServiceDep):
        cmd = LoginUserCommand(identifier=data.identifier, password=data.password)
        token = await service.login(cmd)
        return TokenResponse(access_token=token)
    
    @router.post("/token", response_model=TokenResponse, status_code=status.HTTP_200_OK)
    async def login_form(service: UserServiceDep, form: OAuth2PasswordRequestForm = Depends()):
        cmd = LoginUserCommand(identifier=form.username, password=form.password)
        token = await service.login(cmd)
        return TokenResponse(access_token=token)

    @router.get("/me", response_model=UserRead, status_code=status.HTTP_200_OK)
    async def get_user(user: UserDep):
        return user

    @router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
    async def delete_user(user: UserDep, service: UserServiceDep):
        await service.delete(user.id)