from sqlalchemy import select
from passlib.context import CryptContext
from db.uow import UnitOfWork
from auth.models import User
from auth.domain import RegisterUserCommand

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

class UserRepository:

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def create_user(self, data: RegisterUserCommand) -> User:
        hashed = pwd_context.hash(data.password)
        user = User(
            email=data.email,
            username=data.username,
            hashed_password=hashed
        )
        self.uow.db.add(user)
        await self.uow.db.flush()
        return user

    async def get_by_email(self, email: str) -> User|None:
        stmt = select(User).where(User.email == email)
        return await self.uow.db.scalar(stmt)

    async def get_by_username(self, username: str) -> User|None:
        stmt = select(User).where(User.username == username)
        return await self.uow.db.scalar(stmt)
    
    async def get_by_user_id(self, id: int) -> User|None:
        stmt = select(User).where(User.id == id)
        return await self.uow.db.scalar(stmt)