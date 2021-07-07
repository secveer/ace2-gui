from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from api.models.analysis import AnalysisCreate, AnalysisRead, AnalysisUpdate, DiscoveredObservable
from api.routes import helpers
from api.routes.node import create_node, update_node
from db import crud
from db.database import get_db
from db.schemas.analysis import Analysis
from db.schemas.analysis_module_type import AnalysisModuleType
from db.schemas.observable_instance import ObservableInstance


router = APIRouter(
    prefix="/analysis",
    tags=["Analysis"],
)


#
# CREATE
#


def create_analysis(
    analysis: AnalysisCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    # Create the new analysis Node using the data from the request
    new_analysis: Analysis = create_node(node_create=analysis, db_node_type=Analysis, db=db)

    # If an analysis module type was given, get it from the database to use with the new analysis
    if analysis.analysis_module_type:
        new_analysis.analysis_module_type = crud.read(
            uuid=analysis.analysis_module_type, db_table=AnalysisModuleType, db=db
        )

    # If discovered observables were given, get them from the database and use them in the new analysis
    db_discovered_observables = []
    if analysis.discovered_observables:
        db_discovered_observables = crud.read_by_uuids(
            uuids=analysis.discovered_observables, db_table=ObservableInstance, db=db
        )
    new_analysis.discovered_observables = db_discovered_observables

    # Save the new analysis to the database
    db.add(new_analysis)
    crud.commit(db)

    response.headers["Content-Location"] = request.url_for(
        "get_analysis", uuid=new_analysis.uuid
    )


helpers.api_route_create(router, create_analysis)


#
# READ
#


# def get_all_analysis(db: Session = Depends(get_db)):
#     return crud.read_all(db_table=Analysis, db=db)


def get_analysis(uuid: UUID, db: Session = Depends(get_db)):
    return crud.read(uuid=uuid, db_table=Analysis, db=db)


# It does not make sense to have a get_all_analysis route at this point (and certainly not without pagination).
# helpers.api_route_read_all(router, get_all_analysis, List[AnalysisRead])
helpers.api_route_read(router, get_analysis, AnalysisRead)


#
# UPDATE
#


def update_analysis(
    uuid: UUID,
    analysis: AnalysisUpdate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    # Update the Node attributes
    db_analysis: Analysis = update_node(node_update=analysis, uuid=uuid, db_table=Analysis, db=db)

    # Get the data that was given in the request and use it to update the database object
    update_data = analysis.dict(exclude_unset=True)

    if "analysis_module_type" in update_data:
        db_analysis_module_type = crud.read(
            uuid=update_data["analysis_module_type"], db_table=AnalysisModuleType, db=db
        )
        db_analysis.analysis_module_type = db_analysis_module_type

    if "details" in update_data:
        db_analysis.details = update_data["details"]

    if "discovered_observables" in update_data:
        # Discovered observables are appended to the existing ones and do not replace them.
        db_discovered_observables = crud.read_by_uuids(
            uuids=update_data["discovered_observables"], db_table=ObservableInstance, db=db
        )
        db_analysis.discovered_observables += db_discovered_observables

    if "error_message" in update_data:
        db_analysis.error_message = update_data["error_message"]

    if "stack_trace" in update_data:
        db_analysis.stack_trace = update_data["stack_trace"]

    if "summary" in update_data:
        db_analysis.summary = update_data["summary"]

    crud.commit(db)

    response.headers["Content-Location"] = request.url_for("get_analysis", uuid=uuid)


helpers.api_route_update(router, update_analysis)


#
# DELETE
#


def delete_analysis(uuid: UUID, db: Session = Depends(get_db)):
    """
    Deletes an analysis from the database, but only if it was manually added by an analyst. This is to prevent
    deleting analyses that were automatically added by the ACE Core.
    """

    db_analysis: Analysis = crud.read(uuid=uuid, db_table=Analysis, db=db)
    if db_analysis.manual is True:
        crud.delete(uuid=uuid, db_table=Analysis, db=db)
    else:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=f"{uuid} is not a manually created analysis")


def delete_analysis_discovered_observable(
    analysis_uuid: UUID,
    discovered_observable: DiscoveredObservable,
    db: Session = Depends(get_db)
):
    # Read the current analysis from the database
    db_analysis: Analysis = crud.read(uuid=analysis_uuid, db_table=Analysis, db=db)

    # Read the current discovered observable from the database
    db_discovered_observable: ObservableInstance = crud.read(
        uuid=discovered_observable.uuid, db_table=ObservableInstance, db=db
    )

    # Raise an exception if this discovered observable is not in this analysis.
    if db_discovered_observable not in db_analysis.discovered_observables:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"The discovered observable {discovered_observable.uuid} does not exist in analysis {analysis_uuid}"
        )

    # Raise an exception if this discovered observable was not manually added by an analyst
    # TODO: Figure out how to best add this return value to the API route created by the helper.
    if not db_discovered_observable.manual:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            detail="Unable to remove discovered observable that was not manually added"
        )

    db_analysis.discovered_observables.remove(db_discovered_observable)

    crud.commit(db)


helpers.api_route_delete(router, delete_analysis)
helpers.api_route_delete(router, delete_analysis_discovered_observable, path="/{analysis_uuid}/discovered_observable")
