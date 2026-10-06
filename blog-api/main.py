import logging
from fastapi import FastAPI, Request, Depends
from contextlib import asynccontextmanager
import time
from api.v1.router import router as v1_router
from middleware import CustomHeaderMiddleware
from storage import posts
from typing import Annotated, Protocol
from repository import LaboratoryRepo, ProdLaboratoryRepo, Stub
from core.exception_handlers import register_exception_handlers

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
register_exception_handlers(app)
app.include_router(v1_router)
app.add_middleware(CustomHeaderMiddleware, header_value='Production-Mode')
app.dependency_overrides[Stub(LaboratoryRepo)] = lambda: ProdLaboratoryRepo()

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

@app.get('/lab_repo')
async def lab_repo(repo: Annotated[LaboratoryRepo, Depends(Stub(LaboratoryRepo))]):
    return await repo.get_available_laboratory()