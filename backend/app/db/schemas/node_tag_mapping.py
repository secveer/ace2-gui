from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.dialects.postgresql import UUID

from db.database import Base


node_tag_mapping = Table("node_tag_mapping", Base.metadata,
    Column("node_uuid", UUID(as_uuid=True), ForeignKey("node.uuid"), index=True, primary_key=True),
    Column("tag_id", Integer, ForeignKey("tag.id"), primary_key=True)
)