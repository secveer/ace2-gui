from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session
from typing import List

from api.models.alert_queue import AlertQueueCreate, AlertQueueRead, AlertQueueUpdate
from api.routes import (
    api_route_create,
    api_route_read,
    api_route_read_all,
    api_route_update,
    api_route_delete,
)
from db import crud
from db.database import get_db
from db.schemas.alert_queue import AlertQueue


router = APIRouter(
    prefix="/alert_queue",
    tags=["Alert Queue"],
)


#
# CREATE
#


def create_alert_queue(
    alert_queue: AlertQueueCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    crud.create(
        obj=alert_queue,
        db_table=AlertQueue,
        response_location="get_alert_queue",
        db=db,
        request=request,
        response=response,
    )


api_route_create(router, create_alert_queue)


#
# READ
#


def get_all_alert_queues(db: Session = Depends(get_db)):
    return crud.read_all(db_table=AlertQueue, db=db)


def get_alert_queue(id: int, db: Session = Depends(get_db)):
    return crud.read_by_id(id=id, db_table=AlertQueue, db=db)


api_route_read_all(router, get_all_alert_queues, List[AlertQueueRead])
api_route_read(router, get_alert_queue, AlertQueueRead)


#
# UPDATE
#


def update_alert_queue(
    id: int,
    alert_queue: AlertQueueUpdate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    crud.update_by_id(
        id=id,
        obj=alert_queue,
        db_table=AlertQueue,
        response_location="get_alert_queue",
        db=db,
        request=request,
        response=response,
    )


api_route_update(router, update_alert_queue)


#
# DELETE
#


def delete_alert_queue(id: int, db: Session = Depends(get_db)):
    crud.delete_by_id(id=id, db_table=AlertQueue, db=db)


api_route_delete(router, delete_alert_queue)
