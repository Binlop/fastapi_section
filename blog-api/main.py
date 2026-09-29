import logging
from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
import time
from api.v1.router import router as v1_router
from storage import posts

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Blog запущен. Загружено постов: {len(posts)}")
    yield
    logger.info("Blog останавливается. До встречи!")

app = FastAPI(title="Blog API", lifespan=lifespan)

@app.middleware('http')
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter()
    response.headers["X-Process-Time"] = str(process_time)
    return response

@app.get("/")
async def root():
    return {"status": "API is running"}

@app.get("/ping")
async def health():
    return {"status": "ok", "message": "Pong!"} 