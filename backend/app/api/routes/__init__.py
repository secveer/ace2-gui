from fastapi import APIRouter
from api.routes.ping import router as ping_router
from api.routes.tag import router as tag_router

router = APIRouter()

router.include_router(ping_router, prefix="/ping", tags=["ping"])
router.include_router(tag_router, prefix="/tag", tags=["tag"])