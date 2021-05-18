from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session
from typing import List

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
    id = crud.create(obj=disposition, db_table=Disposition, db=db)

    response.headers["Content-Location"] = request.url_for("get_disposition", id=id)


helpers.api_route_create(router, create_disposition)


#
# READ
#


def get_all_dispositions(db: Session = Depends(get_db)):
    return crud.read_all(db_table=Disposition, db=db)


def get_disposition(id: int, db: Session = Depends(get_db)):
    return crud.read_by_id(id=id, db_table=Disposition, db=db)


helpers.api_route_read_all(router, get_all_dispositions, List[DispositionRead])
helpers.api_route_read(router, get_disposition, DispositionRead)


#
# UPDATE
#


def update_disposition(
    id: int,
    disposition: DispositionUpdate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    crud.update_by_id(id=id, obj=disposition, db_table=Disposition, db=db)

    response.headers["Content-Location"] = request.url_for("get_disposition", id=id)


helpers.api_route_update(router, update_disposition)


#
# DELETE
#


def delete_disposition(id: int, db: Session = Depends(get_db)):
    crud.delete_by_id(id=id, db_table=Disposition, db=db)


helpers.api_route_delete(router, delete_disposition)
