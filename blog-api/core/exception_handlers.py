from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from core.exceptions import InvalidCredentialsError, InvalidTokenError, EmailAlreadyExistsError

def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(InvalidCredentialsError)
    async def invalid_credentials_handler(request: Request, exc: InvalidCredentialsError):
        return JSONResponse(
            status_code=401,
            content={'detail': 'Неверный email или пароль'},
            headers={"WWW-Authenticate": "Bearer"},
        )

    @app.exception_handler(InvalidTokenError)
    async def invalid_token_handler(request: Request, exc: InvalidTokenError):
        return JSONResponse(
            status_code=401,
            content={'detail': 'Токен невалиден или истёк'},
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    @app.exception_handler(EmailAlreadyExistsError)
    async def email_exists_handler(request: Request, exc: EmailAlreadyExistsError):
        return JSONResponse(
            status_code=409,
            content={"detail": "Email уже занят"},
        )

    