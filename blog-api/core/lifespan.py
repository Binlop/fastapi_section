import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI

from storage import posts

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Blog запущен. Загружено постов: %d", len(posts))
    yield
    logger.info("Blog останавливается. До встречи!")