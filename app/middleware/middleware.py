from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.utils.loggers import logger

class LogginMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        log_dict = {
            'url' : request.url.path,
            'method' : request.method
        }
        logger.info(log_dict)

        response = await call_next(request)
        return response
