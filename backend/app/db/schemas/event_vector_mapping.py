from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.dialects.postgresql import UUID

from db.database import Base


event_vector_mapping = Table("event_vector_mapping", Base.metadata,
    Column("event_uuid", UUID(as_uuid=True), ForeignKey("event.uuid"), index=True, primary_key=True),
    Column("vector_id", Integer, ForeignKey("event_vector.id"), primary_key=True)
)