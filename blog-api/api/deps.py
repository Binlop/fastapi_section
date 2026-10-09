from collections.abc import AsyncGenerator
from dataclasses import dataclass
from typing import Annotated
from fastapi import Depends, Query
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from core.security import verify_token
from core.exceptions import InvalidTokenError
from db.session import AsyncSession
from db.uow import UnitOfWork
from auth.repository import UserRepository
from posts.repository import PostRepository
from posts.service import PostService
from auth.service import UserService
from auth.models import User
from structlog.contextvars import bind_contextvars

@dataclass
class Pagination:
    limit: int = 10
    offset: int = 0

def get_pagination(
        limit: int = Query(10, ge=1, le=100, description="Сколько записей вернуть"),
        offset: int = Query(0, ge=0, description="Сколько записей пропустить"),
) -> Pagination:
    return Pagination(limit=limit, offset=offset)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

async def get_uow() -> AsyncGenerator[UnitOfWork, None]:
    async with AsyncSession() as session:
        async with UnitOfWork(session) as uow:
            yield uow

def get_user_repository(uow: UnitOfWork = Depends(get_uow)) -> UserRepository:
    return UserRepository(uow)

def get_user_service(uow: UnitOfWork = Depends(get_uow)) -> UserService:
    return UserService(uow)

def get_post_repository(uow: UnitOfWork = Depends(get_uow)) -> PostRepository:
    return PostRepository(uow)

def get_post_service(uow: UnitOfWork = Depends(get_uow)) -> PostService:
    return PostService(uow)

UserRepoDep = Annotated[UserRepository, Depends(get_user_repository)]
UserServiceDep = Annotated[UserService, Depends(get_user_service)]

PaginationDep = Annotated[Pagination, Depends(get_pagination)]

async def get_current_user(
    repo: UserRepoDep,
    token: str = Depends(oauth2_scheme),
) -> User:
    payload = verify_token(token)
    sub = payload.get("sub")
    try:
        sub = int(sub)
    except Exception as e:
        raise InvalidTokenError()
    user = await repo.get_by_user_id(id=sub)
    if not user or not user.is_active:
        raise InvalidTokenError()
    bind_contextvars(user_id=user.id)
    return user

UserDep = Annotated[User, Depends(get_current_user)]

