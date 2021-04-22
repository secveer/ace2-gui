from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.database import Base
from db.schemas.helpers import utcnow


class Comment(Base):
    __tablename__ = "comment"

    id = Column(Integer, primary_key=True)

    insert_time = Column(DateTime, server_default=utcnow())

    node_uuid = Column(UUID(as_uuid=True), ForeignKey("node.uuid"))

    user_uuid = Column(UUID(as_uuid=True), ForeignKey("user.uuid"))

    user = relationship("User", foreign_keys=[user_uuid])

    value = Column(String)

    __table_args__ = (
        Index("node_uuid", node_uuid),
    )