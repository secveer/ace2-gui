from typing import Any, Callable
from fastapi import APIRouter, Response, status


#
# CREATE
#


def api_route_create(router: APIRouter, endpoint: Callable):
    router.add_api_route(
        path="",
        endpoint=endpoint,
        methods=["POST"],
        response_class=Response,
        responses={
            status.HTTP_201_CREATED: {
                "headers": {
                    "Content-Location": {
                        "description": "The path to retrieve the resource"
                    },
                },
            },
            status.HTTP_409_CONFLICT: {"description": "The resource already exists"},
        },
        status_code=status.HTTP_201_CREATED,
    )


#
# READ
#


def api_route_read_all(router: APIRouter, endpoint: Callable, response_model: Any):
    router.add_api_route(
        path="",
        endpoint=endpoint,
        methods=["GET"],
        response_model=response_model,
    )


def api_route_read(router: APIRouter, endpoint: Callable, response_model: Any):
    router.add_api_route(
        path="/{id}",
        endpoint=endpoint,
        methods=["GET"],
        response_model=response_model,
        responses={
            status.HTTP_404_NOT_FOUND: {"description": "The ID was not found"},
        },
    )


#
# UPDATE
#


def api_route_update(router: APIRouter, endpoint: Callable):
    router.add_api_route(
        path="/{id}",
        endpoint=endpoint,
        methods=["PUT"],
        responses={
            status.HTTP_204_NO_CONTENT: {
                "headers": {
                    "Content-Location": {
                        "description": "The path to retrieve the resource"
                    }
                },
            },
            status.HTTP_400_BAD_REQUEST: {
                "description": "The database returned an IntegrityError"
            },
            status.HTTP_404_NOT_FOUND: {"description": "The ID was not found"},
        },
        status_code=status.HTTP_204_NO_CONTENT,
    )


#
# DELETE
#


def api_route_delete(router: APIRouter, endpoint: Callable):
    router.add_api_route(
        path="/{id}",
        endpoint=endpoint,
        methods=["DELETE"],
        responses={
            status.HTTP_400_BAD_REQUEST: {
                "description": "Unable to delete the alert queue"
            },
        },
        status_code=status.HTTP_204_NO_CONTENT,
    )


from api.routes.alert import router as alert_router
from api.routes.alert_queue import router as alert_queue_router
from api.routes.disposition import router as disposition_router
from api.routes.ping import router as ping_router


router = APIRouter()

router.include_router(alert_router)
router.include_router(alert_queue_router)
router.include_router(disposition_router)
router.include_router(ping_router)
