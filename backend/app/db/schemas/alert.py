from sqlalchemy import Column, DateTime, ForeignKey, Index, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.schemas.node import Node
from db.schemas.helpers import utcnow


class Alert(Node):
    __tablename__ = "alert"

    uuid = Column(UUID(as_uuid=True), ForeignKey("node.uuid"), primary_key=True)

    analysis_uuid = Column(UUID(as_uuid=True), ForeignKey("analysis.uuid"), nullable=False, unique=True)

    analysis = relationship("Analysis", foreign_keys=[analysis_uuid])

    description = Column(String)

    disposition = relationship("AlertDisposition")

    disposition_uuid = Column(UUID(as_uuid=True), ForeignKey("alert_disposition.uuid"))

    disposition_time = Column(DateTime(timezone=True))

    disposition_user_uuid = Column(UUID(as_uuid=True), ForeignKey("user.uuid"))

    disposition_user = relationship("User", foreign_keys=[disposition_user_uuid])

    event_time = Column(DateTime(timezone=True), server_default=utcnow(), nullable=False)

    event_uuid = Column(UUID(as_uuid=True), ForeignKey("event.uuid"))

    event = relationship("Event", foreign_keys=[event_uuid])

    insert_time = Column(DateTime(timezone=True), server_default=utcnow(), nullable=False)

    instructions = Column(String)

    name = Column(String)

    owner_uuid = Column(UUID(as_uuid=True), ForeignKey("user.uuid"))

    owner = relationship("User", foreign_keys=[owner_uuid])

    queue = relationship("AlertQueue")

    queue_uuid = Column(UUID(as_uuid=True), ForeignKey("alert_queue.uuid"), nullable=False)

    tool = relationship("AlertTool")

    tool_uuid = Column(UUID(as_uuid=True), ForeignKey("alert_tool.uuid"))

    tool_instance = relationship("AlertToolInstance")

    tool_instance_uuid = Column(UUID(as_uuid=True), ForeignKey("alert_tool_instance.uuid"))

    type = relationship("AlertType")

    type_uuid = Column(UUID(as_uuid=True), ForeignKey("alert_type.uuid"), nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "alert",
    }

    # TODO: We need a lot more indices here for when we introduce searching API endpoints.
    __table_args__ = (Index("event_uuid", event_uuid),)
