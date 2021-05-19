from fastapi import APIRouter

from api.routes.alert import router as alert_router
from api.routes.alert_queue import router as alert_queue_router
from api.routes.alert_type import router as alert_type_router
from api.routes.directive import router as directive_router
from api.routes.disposition import router as disposition_router
from api.routes.event_prevention_tool import router as event_prevention_tool_router
from api.routes.ping import router as ping_router


router = APIRouter()

router.include_router(alert_router)
router.include_router(alert_queue_router)
router.include_router(alert_type_router)
router.include_router(directive_router)
router.include_router(disposition_router)
router.include_router(event_prevention_tool_router)
router.include_router(ping_router)
