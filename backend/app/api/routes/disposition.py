from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session
from typing import List

from api.models.disposition import DispositionCreate, DispositionRead, DispositionUpdate
from api.routes import (
    api_route_create,
    api_route_read,
    api_route_read_all,
    api_route_update,
    api_route_delete,
)
from db import crud
from db.database import get_db
from db.schemas.disposition import Disposition


router = APIRouter(
    prefix="/disposition",
    tags=["disposition"],
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
    crud.create(
        obj=disposition,
        db_table=Disposition,
        response_location="get_disposition",
        db=db,
        request=request,
        response=response,
    )


api_route_create(router, create_disposition)


#
# READ
#


def get_all_dispositions(db: Session = Depends(get_db)):
    return crud.read_all(db_table=Disposition, db=db)


def get_disposition(id: int, db: Session = Depends(get_db)):
    return crud.read_by_id(id=id, db_table=Disposition, db=db)


api_route_read_all(router, get_all_dispositions, List[DispositionRead])
api_route_read(router, get_disposition, DispositionRead)


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
    crud.update_by_id(
        id=id,
        obj=disposition,
        db_table=Disposition,
        response_location="get_disposition",
        db=db,
        request=request,
        response=response,
    )


api_route_update(router, update_disposition)


#
# DELETE
#


def delete_disposition(id: int, db: Session = Depends(get_db)):
    crud.delete_by_id(id=id, db_table=Disposition, db=db)


api_route_delete(router, delete_disposition)