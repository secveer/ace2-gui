from fastapi import APIRouter, Response, status
from pydantic import BaseModel
from typing import Callable


#
# CREATE
#


def api_route_create(router: APIRouter, endpoint: Callable):
    router.add_api_route(
        path="",
        endpoint=endpoint,
        methods=["POST"],
        response_class=Response,  # This allows to respond with a 201 and no body listed in the documentation
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


def api_route_read_all(router: APIRouter, endpoint: Callable, response_model: BaseModel):
    router.add_api_route(
        path="",
        endpoint=endpoint,
        methods=["GET"],
        response_model=response_model,
    )


def api_route_read(router: APIRouter, endpoint: Callable, response_model: BaseModel):
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