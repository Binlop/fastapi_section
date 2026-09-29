import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager
from .storage import hotels, rooms

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Hotel запущен. Загружено отелей: {len(hotels)}. Загружено комнат: {len(rooms)}")
    yield
    logger.info("Hotel останавливается. До встречи!")
    
app = FastAPI(title="Hotel Booking API", lifespan=lifespan)

@app.get("/ping")
async def health():
    return {"status": "ok", "message": "Pong!"} 