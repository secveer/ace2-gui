from fastapi import HTTPException, status
from pydantic import BaseModel
from sqlalchemy import delete, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.orm.decl_api import DeclarativeMeta


#
# CREATE
#


def create(obj: BaseModel, db_table: DeclarativeMeta, db: Session) -> int:
    """Creates a new object in the given database table. Returns the new object's ID."""

    new_obj = db_table(**obj.dict())
    db.add(new_obj)

    try:
        db.commit()
        return new_obj.id
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
    """Returns all objects from the given database table."""

    return db.execute(select(db_table)).scalars().all()


def read_by_id(id: int, db_table: DeclarativeMeta, db: Session):
    """Returns the single object with the given ID if it exists, otherwise returns None."""

    result = (
        db.execute(select(db_table).where(db_table.id == id)).scalars().one_or_none()
    )

    if result is None:
        raise HTTPException(status_code=404, detail=f"ID {id} does not exist.")

    return result


#
# UPDATE
#


def update_by_id(id: int, obj: BaseModel, db_table: DeclarativeMeta, db: Session):
    """Updates the object with the given ID in the database."""

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
            raise HTTPException(status_code=404, detail=f"ID {id} does not exist.")

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
    """Deletes the object with the given ID from the database."""

    # NOTE: This will need to be updated to account for foreign key constraint errors.
    result = db.execute(delete(db_table).where(db_table.id == id))

    if result.rowcount != 1:
        raise HTTPException(
            status_code=400,
            detail=f"Unable to delete ID {id} or it does not exist.",
        )
