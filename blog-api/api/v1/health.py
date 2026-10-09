from fastapi import APIRouter

router = APIRouter(prefix="", tags=['Health'])

@router.get("/")
async def root():
    return {"status": "API is running"}

@router.get("/ping")
async def health():
    return {"status": "ok", "message": "Pong!"} 