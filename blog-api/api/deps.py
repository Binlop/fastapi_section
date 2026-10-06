from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from typing import TypedDict
from db.session import get_async_db
from core.security import verify_token
from core.exceptions import InvalidTokenError
import storage

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

class User(TypedDict):
    id: int
    email: str
    hashed_password: str
    is_active: bool

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_async_db),
) -> User:
    payload = verify_token(token)
    print(payload)
    if payload is None:
        raise InvalidTokenError()
    sub = payload.get("sub")
    try:
        sub = int(sub)
    except Exception as e:
        raise InvalidTokenError()
    user = next((u for u in storage.users if u['id'] == sub), None)
    # user = await db.get(User, payload.get("sub"))
    if user is None:
        print('не нашли пользователя')
        raise InvalidTokenError()
    return user
