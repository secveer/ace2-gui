from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.dialects.postgresql import UUID

from db.database import Base


event_remediation_mapping = Table("event_remediation_mapping", Base.metadata,
    Column("event_uuid", UUID(as_uuid=True), ForeignKey("event.uuid"), index=True, primary_key=True),
    Column("remediation_id", Integer, ForeignKey("event_remediation.id"), primary_key=True)
)