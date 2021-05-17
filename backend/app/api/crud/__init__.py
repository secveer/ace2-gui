from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from pydantic import BaseModel
from sqlalchemy import delete, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.orm.decl_api import DeclarativeMeta
from typing import Any, List


#
# CREATE
#


def create(
    obj: BaseModel,
    db_table: DeclarativeMeta,
    response_location: str,
    db: Session,
    request: Request,
    response: Response,
):
    new_obj = db_table(**obj.dict())
    db.add(new_obj)

    try:
        db.commit()
        response.headers["Content-Location"] = request.url_for(
            response_location, id=new_obj.id
        )
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"A similiar object already exists",
        )


#
# READ
#


def read_all(db_table: DeclarativeMeta, db: Session):
    return db.execute(select(db_table)).scalars().all()


def read_by_id(db_table: DeclarativeMeta, id: int, db: Session):
    result = (
        db.execute(select(db_table).where(db_table.id == id)).scalars().one_or_none()
    )

    if result is None:
        raise HTTPException(status_code=404, detail=f"ID {id} does not exist.")

    return result


#
# UPDATE
#


def update_by_id(
    id: int,
    obj: BaseModel,
    db_table: DeclarativeMeta,
    response_location: str,
    db: Session,
    request: Request,
    response: Response,
):

# Try to perform the update
    try:
        result = db.execute(
            update(db_table)
            .where(db_table.id == id)
            .values(
                # exclude_unset is needed for update routes so that any values in the Pydantic model
                # that are not being updated are not set to None. Instead they will be removed from the dict.
                **obj.dict(exclude_unset=True)
            )
        )

        # Verify a row was actually updated
        if result.rowcount != 1:
            raise HTTPException(
                status_code=404, detail=f"ID {id} does not exist."
            )

        # Set the Content-Location header to get the object
        response.headers["Content-Location"] = request.url_for(response_location, id=id)

    # An IntegrityError will happen if value already exists or was set to None
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Got an IntegrityError while updating ID {id}.",
        )


#
# DELETE
#


def delete_by_id(id: int, db_table: DeclarativeMeta, db: Session):
    # NOTE: This will need to be updated to account for foreign key constraint errors.
    result = db.execute(delete(db_table).where(db_table.id == id))

    if result.rowcount != 1:
        raise HTTPException(
            status_code=400,
            detail=f"Unable to delete ID {id} or it does not exist.",
        )
