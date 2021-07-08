from datetime import datetime
from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from api.models.alert import AlertCreate, AlertRead, AlertUpdate
from api.models.analysis import AnalysisCreate
from api.routes import helpers
from api.routes.node import create_node, update_node
from db import crud
from db.database import get_db
from db.schemas.alert import Alert
from db.schemas.alert_disposition import AlertDisposition
from db.schemas.alert_queue import AlertQueue
from db.schemas.alert_tool import AlertTool
from db.schemas.alert_tool_instance import AlertToolInstance
from db.schemas.alert_type import AlertType
from db.schemas.analysis import Analysis
from db.schemas.event import Event
from db.schemas.user import User


router = APIRouter(
    prefix="/alert",
    tags=["Alert"],
)


#
# CREATE
#


def create_alert(
    alert: AlertCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    # Create the new alert Node using the data from the request
    new_alert: Alert = create_node(node_create=alert, db_node_type=Alert, db=db)

    # Set the automatic alert properties
    new_alert.insert_time = datetime.utcnow()

    # Set the required alert properties
    new_alert.queue = crud.read_by_value(value=alert.queue, db_table=AlertQueue, db=db)
    new_alert.type = crud.read_by_value(value=alert.type, db_table=AlertType, db=db)

    # Set the various optional alert properties if they were given in the request.
    if alert.owner:
        new_alert.owner = crud.read_user_by_username(username=alert.owner, db=db)

    if alert.tool:
        new_alert.tool = crud.read_by_value(value=alert.tool, db_table=AlertTool, db=db)

    if alert.tool_instance:
        new_alert.tool_instance = crud.read_by_value(value=alert.tool_instance, db_table=AlertToolInstance, db=db)

    # Alerts must point to an Analysis, so if we get this far without any errors, a new Analysis needs to be created.
    new_alert.analysis = create_node(node_create=AnalysisCreate(), db_node_type=Analysis, db=db)

    # Save the new alert (including the new analysis) to the database
    db.add(new_alert)
    crud.commit(db)

    response.headers["Content-Location"] = request.url_for("get_alert", uuid=new_alert.uuid)


helpers.api_route_create(router, create_alert)


#
# READ
#


# def get_all_alerts(db: Session = Depends(get_db)):
#     return crud.read_all(db_table=Alert, db=db)


def get_alert(uuid: UUID, db: Session = Depends(get_db)):
    return crud.read(uuid=uuid, db_table=Alert, db=db)


# It does not make sense to have a get_all_alerts route at this point (and certainly not without pagination).
# helpers.api_route_read_all(router, get_all_alerts, List[AlertRead])
helpers.api_route_read(router, get_alert, AlertRead)


#
# UPDATE
#


def update_alert(
    uuid: UUID,
    alert: AlertUpdate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    # Update the Node attributes
    db_alert: Alert = update_node(node_update=alert, uuid=uuid, db_table=Alert, db=db)

    # Get the data that was given in the request and use it to update the database object
    update_data = alert.dict(exclude_unset=True)

    if "description" in update_data:
        db_alert.description = update_data["description"]

    if "disposition" in update_data:
        db_alert.disposition = crud.read_by_value(value=update_data["disposition"], db_table=AlertDisposition, db=db)

    if "event" in update_data:
        db_alert.event = crud.read(uuid=update_data["event"], db_table=Event, db=db)

    if "event_time" in update_data:
        db_alert.event_time = update_data["event_time"]

    if "instructions" in update_data:
        db_alert.instructions = update_data["instructions"]

    if "name" in update_data:
        db_alert.name = update_data["name"]

    if "owner" in update_data:
        db_alert.owner = crud.read_user_by_username(username=update_data["owner"], db=db)

    if "queue" in update_data:
        db_alert.queue = crud.read_by_value(value=update_data["queue"], db_table=AlertQueue, db=db)

    if "tool" in update_data:
        db_alert.tool = crud.read_by_value(value=update_data["tool"], db_table=AlertTool, db=db)

    if "tool_instance" in update_data:
        db_alert.tool_instance = crud.read_by_value(
            value=update_data["tool_instance"],
            db_table=AlertToolInstance,
            db=db,
        )

    if "type" in update_data:
        db_alert.type = crud.read_by_value(value=update_data["type"], db_table=AlertType, db=db)

    crud.commit(db)

    response.headers["Content-Location"] = request.url_for("get_alert", uuid=uuid)


helpers.api_route_update(router, update_alert)


#
# DELETE
#


# We currently do not support deleting any Nodes.
