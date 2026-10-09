from passlib.context import CryptContext
from core.exceptions import InvalidCredentialsError, EmailAlreadyExistsError, UsernameAlreadyExistsError, UserAlreadyDeletedError
from core.security import create_access_token
from db.uow import UnitOfWork
from auth.models import User
from auth.exceptions import UserNotFoundError
from auth.repository import UserRepository
from auth.domain import RegisterUserCommand, LoginUserCommand

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

class UserService:

    def __init__(self, uow: UnitOfWork):
        self.user_repository = UserRepository(uow)

    async def register(self, cmd: RegisterUserCommand) -> User:
        if await self.user_repository.get_by_email(cmd.email):
            raise EmailAlreadyExistsError()
        if await self.user_repository.get_by_username(cmd.username):
            raise UsernameAlreadyExistsError()
        user = await self.user_repository.create_user(cmd)
        return user

    async def login(self, cmd: LoginUserCommand) -> User:
        if "@" in cmd.identifier:
            user = await self.user_repository.get_by_email(cmd.identifier)
        else:
            user = await self.user_repository.get_by_username(cmd.identifier)
        if not user or not pwd_context.verify(secret=cmd.password, hash=user.hashed_password):
            raise InvalidCredentialsError()
        data_to_token = {'sub': str(user.id)}
        token = create_access_token(data_to_token)
        return token

    async def delete(self, user_id: int) -> None:
        user = await self.user_repository.get_by_user_id(id=user_id)
        if user is None:
            raise UserNotFoundError(user_id)
        if not user.is_active:
            raise UserAlreadyDeletedError(user_id)
        user.is_active = False
        