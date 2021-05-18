from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from api.models.disposition import DispositionCreate, DispositionRead, DispositionUpdate
from api.routes import helpers
from db import crud
from db.database import get_db
from db.schemas.disposition import Disposition


router = APIRouter(
    prefix="/disposition",
    tags=["Disposition"],
)


#
# CREATE
#


def create_disposition(
    disposition: DispositionCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    uuid = crud.create(obj=disposition, db_table=Disposition, db=db)

    response.headers["Content-Location"] = request.url_for("get_disposition", uuid=uuid)


helpers.api_route_create(router, create_disposition)


#
# READ
#


def get_all_dispositions(db: Session = Depends(get_db)):
    return crud.read_all(db_table=Disposition, db=db)


def get_disposition(uuid: UUID, db: Session = Depends(get_db)):
    return crud.read(uuid=uuid, db_table=Disposition, db=db)


helpers.api_route_read_all(router, get_all_dispositions, List[DispositionRead])
helpers.api_route_read(router, get_disposition, DispositionRead)


#
# UPDATE
#


def update_disposition(
    uuid: UUID,
    disposition: DispositionUpdate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    crud.update(uuid=uuid, obj=disposition, db_table=Disposition, db=db)

    response.headers["Content-Location"] = request.url_for("get_disposition", uuid=uuid)


helpers.api_route_update(router, update_disposition)


#
# DELETE
#


def delete_disposition(uuid: UUID, db: Session = Depends(get_db)):
    crud.delete(uuid=uuid, db_table=Disposition, db=db)


helpers.api_route_delete(router, delete_disposition)
