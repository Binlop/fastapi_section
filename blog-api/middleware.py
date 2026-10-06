from fastapi import Request, FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

class CustomHeaderMiddleware(BaseHTTPMiddleware):

    def __init__(self, app, dispatch = None, header_value: str = None):
        super().__init__(app, dispatch)
        self.header_value = header_value

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers['X-Environment-Mode'] = self.header_value
        return response