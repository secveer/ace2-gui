from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.dialects.postgresql import UUID

from db.database import Base


node_directive_mapping = Table("node_directive_mapping", Base.metadata,
    Column("node_uuid", UUID(as_uuid=True), ForeignKey("node.uuid"), index=True, primary_key=True),
    Column("directive_id", Integer, ForeignKey("directive.id"), primary_key=True)
)