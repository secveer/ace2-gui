from fastapi import APIRouter


router = APIRouter()

@router.get("/")
def ping() -> dict:
    return {"ping": "pong"}