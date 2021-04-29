from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.dialects.postgresql import UUID

from db.database import Base


user_role_mapping = Table("user_role_mapping", Base.metadata,
    Column("user_uuid", UUID(as_uuid=True), ForeignKey("user.uuid"), index=True, primary_key=True),
    Column("role_id", Integer, ForeignKey("role.id"), primary_key=True)
)