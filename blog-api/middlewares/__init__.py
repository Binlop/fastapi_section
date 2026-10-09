from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


class CustomHeaderMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, header_value: str = "Production-Mode"):
        super().__init__(app)
        self.header_value = header_value

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Custom-Header"] = self.header_value
        return response