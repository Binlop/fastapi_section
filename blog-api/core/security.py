from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError, ExpiredSignatureError

SECRET_KEY = "e91228ce7ab6601937e037dc791248a167327b38413a8ca4ede09ceafc50ce9e"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    now = datetime.now(timezone.utc)
    to_encode.update({
            "exp": now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
            "iat": now,
            'token_type': 'bearer'
        })
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> dict | None:
    try:
        print(token)
        print(type(token))
        token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(token)
        return token
    except ExpiredSignatureError:
        print('Token expired')
        return None
    except JWTError as e:
        print(f"Invalid token: {e}")
        return None