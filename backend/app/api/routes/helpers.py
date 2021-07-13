from fastapi import APIRouter, Response, status
from pydantic import BaseModel
from typing import Callable


#
# CREATE
#


def api_route_create(router: APIRouter, endpoint: Callable, path: str = "/"):
    router.add_api_route(
        path=path,
        endpoint=endpoint,
        methods=["POST"],
        response_class=Response,  # This allows to respond with a 201 and no body listed in the documentation
        responses={
            status.HTTP_201_CREATED: {
                "headers": {
                    "Content-Location": {"description": "The path to retrieve the resource"},
                },
            },
            status.HTTP_409_CONFLICT: {"description": "The resource already exists"},
        },
        status_code=status.HTTP_201_CREATED,
    )


#
# READ
#


# The trailing slash is required due to how some of the API endpoints are organized. For instance, there is a
# /user/ endpoint and a /user/role/ endpoint. If you were to drop the trailing slash and tried to access /user/role,
# it would not know if you wanted to access the get_all_user_roles endpoint or were trying to access the "role" user,
# which is invalid since you must supply a UUID in order to retrieve a user.
def api_route_read_all(router: APIRouter, endpoint: Callable, response_model: BaseModel, path: str = "/"):
    router.add_api_route(
        path=path,
        endpoint=endpoint,
        methods=["GET"],
        response_model=response_model,
    )


def api_route_read(router: APIRouter, endpoint: Callable, response_model: BaseModel, path: str = "/{uuid}"):
    router.add_api_route(
        path=path,
        endpoint=endpoint,
        methods=["GET"],
        response_model=response_model,
        responses={
            status.HTTP_404_NOT_FOUND: {"description": "The UUID was not found"},
        },
    )


#
# UPDATE
#


def api_route_update(router: APIRouter, endpoint: Callable, path: str = "/{uuid}"):
    router.add_api_route(
        path=path,
        endpoint=endpoint,
        methods=["PATCH"],
        responses={
            status.HTTP_204_NO_CONTENT: {
                "headers": {"Content-Location": {"description": "The path to retrieve the resource"}},
            },
            status.HTTP_404_NOT_FOUND: {"description": "The UUID was not found"},
            status.HTTP_409_CONFLICT: {"description": "The database returned an IntegrityError"},
        },
        status_code=status.HTTP_204_NO_CONTENT,
    )


#
# DELETE
#


def api_route_delete(router: APIRouter, endpoint: Callable, path: str = "/{uuid}"):
    router.add_api_route(
        path=path,
        endpoint=endpoint,
        methods=["DELETE"],
        responses={
            status.HTTP_400_BAD_REQUEST: {"description": "Unable to delete the alert queue"},
        },
        status_code=status.HTTP_204_NO_CONTENT,
    )
