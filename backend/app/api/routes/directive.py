from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from api.models.directive import DirectiveCreate, DirectiveRead, DirectiveUpdate
from api.routes import helpers
from db import crud
from db.database import get_db
from db.schemas.directive import Directive


router = APIRouter(
    prefix="/directive",
    tags=["Directive"],
)


#
# CREATE
#


def create_directive(
    directive: DirectiveCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    uuid = crud.create(obj=directive, db_table=Directive, db=db)

    response.headers["Content-Location"] = request.url_for("get_directive", uuid=uuid)


helpers.api_route_create(router, create_directive)


#
# READ
#


def get_all_directives(db: Session = Depends(get_db)):
    return crud.read_all(db_table=Directive, db=db)


def get_directive(uuid: UUID, db: Session = Depends(get_db)):
    return crud.read(uuid=uuid, db_table=Directive, db=db)


helpers.api_route_read_all(router, get_all_directives, List[DirectiveRead])
helpers.api_route_read(router, get_directive, DirectiveRead)


#
# UPDATE
#


def update_directive(
    uuid: UUID,
    directive: DirectiveUpdate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    crud.update(uuid=uuid, obj=directive, db_table=Directive, db=db)

    response.headers["Content-Location"] = request.url_for("get_directive", uuid=uuid)


helpers.api_route_update(router, update_directive)


#
# DELETE
#


def delete_directive(uuid: UUID, db: Session = Depends(get_db)):
    crud.delete(uuid=uuid, db_table=Directive, db=db)


helpers.api_route_delete(router, delete_directive)
