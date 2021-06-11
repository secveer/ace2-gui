from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from api.models.node_threat import NodeThreatCreate, NodeThreatRead, NodeThreatUpdate
from api.routes import helpers
from db import crud
from db.database import get_db
from db.schemas.node_threat import NodeThreat
from db.schemas.node_threat_type import NodeThreatType


router = APIRouter(
    prefix="/node/threat",
    tags=["Node Threat"],
)


#
# CREATE
#


def create_node_threat(
    node_threat: NodeThreatCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    # Make sure that all the threat types that were given actually exist
    db_threat_types = crud.read_by_values(values=node_threat.types, db_table=NodeThreatType, db=db)

    # Create the new node threat
    new_threat = NodeThreat(**node_threat.dict())

    # Set the threat types on the new node threat
    new_threat.types = db_threat_types

    # Save the new node threat to the database
    db.add(new_threat)
    crud.commit_create(db)

    response.headers["Content-Location"] = request.url_for("get_node_threat", uuid=new_threat.uuid)


helpers.api_route_create(router, create_node_threat)


#
# READ
#


def get_all_node_threats(db: Session = Depends(get_db)):
    return crud.read_all(db_table=NodeThreat, db=db)


def get_node_threat(uuid: UUID, db: Session = Depends(get_db)):
    return crud.read(uuid=uuid, db_table=NodeThreat, db=db)


helpers.api_route_read_all(router, get_all_node_threats, List[NodeThreatRead])
helpers.api_route_read(router, get_node_threat, NodeThreatRead)


#
# UPDATE
#


def update_node_threat(
    uuid: UUID,
    node_threat: NodeThreatUpdate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    # Read the current node threat from the database
    db_node_threat = crud.read(uuid=uuid, db_table=NodeThreat, db=db)

    # Update the description if one was given
    if node_threat.description:
        db_node_threat.description = node_threat.description

    # Update the value if one was given
    if node_threat.value:
        db_node_threat.value = node_threat.value

    # Update the types if they were given
    if node_threat.types:
        # Make sure that all the threat types that were given actually exist
        db_threat_types = crud.read_by_values(values=node_threat.types, db_table=NodeThreatType, db=db)

        # Update the types on the node threat
        db_node_threat.types = db_threat_types

    # Save the updated node threat to the database
    crud.commit_update(db)

    response.headers["Content-Location"] = request.url_for("get_node_threat", uuid=uuid)


helpers.api_route_update(router, update_node_threat)


#
# DELETE
#


def delete_node_threat(uuid: UUID, db: Session = Depends(get_db)):
    crud.delete(uuid=uuid, db_table=NodeThreat, db=db)


helpers.api_route_delete(router, delete_node_threat)
