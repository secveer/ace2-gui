from fastapi import APIRouter

from api.routes.alert import router as alert_router
from api.routes.alert_disposition import router as alert_disposition_router
from api.routes.alert_queue import router as alert_queue_router
from api.routes.alert_type import router as alert_type_router
from api.routes.directive import router as directive_router
from api.routes.event_prevention_tool import router as event_prevention_tool_router
from api.routes.event_remediation import router as event_remediation_router
from api.routes.event_risk_level import router as event_risk_level_router
from api.routes.event_status import router as event_status_router
from api.routes.event_type import router as event_type_router
from api.routes.event_vector import router as event_vector_router
from api.routes.node_history_action import router as node_history_action_router
from api.routes.ping import router as ping_router


router = APIRouter()

router.include_router(alert_router)
router.include_router(alert_disposition_router)
router.include_router(alert_queue_router)
router.include_router(alert_type_router)
router.include_router(directive_router)
router.include_router(event_prevention_tool_router)
router.include_router(event_remediation_router)
router.include_router(event_risk_level_router)
router.include_router(event_status_router)
router.include_router(event_type_router)
router.include_router(event_vector_router)
router.include_router(node_history_action_router)
router.include_router(ping_router)
