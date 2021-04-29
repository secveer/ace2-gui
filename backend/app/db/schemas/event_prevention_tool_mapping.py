from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.dialects.postgresql import UUID

from db.database import Base


event_prevention_tool_mapping = Table("event_prevention_tool_mapping", Base.metadata,
    Column("event_uuid", UUID(as_uuid=True), ForeignKey("event.uuid"), index=True, primary_key=True),
    Column("prevention_tool_id", Integer, ForeignKey("event_prevention_tool.id"), primary_key=True)
)