from passlib.context import CryptContext
from core.exceptions import InvalidCredentialsError
from core.security import create_access_token
from api.deps import User
from auth.schemas import UserRegister
import storage
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def create_user(user: UserRegister) -> User:
    hashed = pwd_context.hash(user.password)
    user_data = {
        "id": storage.next_user_id,
        "email": user.email,
        "password": hashed,
        "is_active": "true",
    }
    storage.users.append(user_data)
    storage.next_user_id += 1
    print(storage.users)
    print(storage.next_user_id)
    user_without_password = user_data.copy()
    user_without_password.pop('password')
    return user_without_password


async def login_user(user: UserRegister) -> dict:
    user_from_db = next((u for u in storage.users if u['email'] == user.email), None)
    if not user_from_db:
        raise InvalidCredentialsError()
    hashed_password = user_from_db['password']
    verify = pwd_context.verify(user.password, hashed_password)
    if not verify:
        raise InvalidCredentialsError()
    data_to_token = {'sub': str(user_from_db['id'])}
    token = create_access_token(data_to_token)
    print(token)
    return token
    
