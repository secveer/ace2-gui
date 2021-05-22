from fastapi import status, APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
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
    threat_types = db.execute(select(NodeThreatType).where(NodeThreatType.value.in_(node_threat.types))).scalars().all()
    for given_type in node_threat.types:
        if not any(given_type == t.value for t in threat_types):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"The {given_type} node threat type does not exist",
            )

    # Create the new node threat
    new_threat = NodeThreat(**node_threat.dict())

    # Set the threat types on the new node threat
    new_threat.types = threat_types

    # Save the new node threat to the database
    db.add(new_threat)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"A similiar object already exists",
        )

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
    crud.update(uuid=uuid, obj=node_threat, db_table=NodeThreat, db=db)

    response.headers["Content-Location"] = request.url_for("get_node_threat", uuid=uuid)


helpers.api_route_update(router, update_node_threat)


#
# DELETE
#


def delete_node_threat(uuid: UUID, db: Session = Depends(get_db)):
    crud.delete(uuid=uuid, db_table=NodeThreat, db=db)


helpers.api_route_delete(router, delete_node_threat)
