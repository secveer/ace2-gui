from fastapi import HTTPException, status
from pydantic import BaseModel
from sqlalchemy import delete as sql_delete, select, update as sql_update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.orm.decl_api import DeclarativeMeta
from uuid import UUID


#
# CREATE
#


def create(obj: BaseModel, db_table: DeclarativeMeta, db: Session) -> int:
    """Creates a new object in the given database table. Returns the new object's UUID.
    Designed to be called only by the API since it raises an HTTPException."""

    new_obj = db_table(**obj.dict())
    db.add(new_obj)

    try:
        db.commit()
        return new_obj.uuid
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


def read(uuid: UUID, db_table: DeclarativeMeta, db: Session):
    """Returns the single object with the given UUID if it exists, otherwise returns None.
    Designed to be called only by the API since it raises an HTTPException."""

    result = (
        db.execute(select(db_table).where(db_table.uuid == uuid)).scalars().one_or_none()
    )

    if result is None:
        raise HTTPException(status_code=404, detail=f"UUID {uuid} does not exist.")

    return result


#
# UPDATE
#


def update(uuid: UUID, obj: BaseModel, db_table: DeclarativeMeta, db: Session):
    """Updates the object with the given UUID in the database.
    Designed to be called only by the API since it raises an HTTPException."""

    # Try to perform the update
    try:
        result = db.execute(
            sql_update(db_table)
            .where(db_table.uuid == uuid)
            .values(
                # exclude_unset is needed for update routes so that any values in the Pydantic model
                # that are not being updated are not set to None. Instead they will be removed from the dict.
                **obj.dict(exclude_unset=True)
            )
        )

        # Verify a row was actually updated
        if result.rowcount != 1:
            raise HTTPException(status_code=404, detail=f"UUID {uuid} does not exist.")

    # An IntegrityError will happen if value already exists or was set to None
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Got an IntegrityError while updating UUID {uuid}.",
        )


#
# DELETE
#


def delete(uuid: UUID, db_table: DeclarativeMeta, db: Session):
    """Deletes the object with the given UUID from the database.
    Designed to be called only by the API since it raises an HTTPException."""

    # NOTE: This will need to be updated to account for foreign key constraint errors.
    result = db.execute(sql_delete(db_table).where(db_table.uuid == uuid))

    if result.rowcount != 1:
        raise HTTPException(
            status_code=400,
            detail=f"Unable to delete UUID {uuid} or it does not exist.",
        )
