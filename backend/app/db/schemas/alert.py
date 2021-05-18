from sqlalchemy import Column, DateTime, ForeignKey, Index, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.schemas.analysis import Analysis
from db.schemas.helpers import utcnow


class Alert(Analysis):
    __tablename__ = "alert"

    uuid = Column(UUID(as_uuid=True), ForeignKey("analysis.uuid"), primary_key=True)

    alert_type = relationship("AlertType")

    alert_type_uuid = Column(UUID(as_uuid=True), ForeignKey("alert_type.uuid"))

    disposition = relationship("Disposition")

    disposition_uuid = Column(UUID(as_uuid=True), ForeignKey("disposition.uuid"))
    
    disposition_time = Column(DateTime)

    disposition_user_uuid = Column(UUID(as_uuid=True), ForeignKey("user.uuid"))

    disposition_user = relationship("User", foreign_keys=[disposition_user_uuid])

    event_uuid = Column(UUID(as_uuid=True), ForeignKey("event.uuid"))

    event = relationship("Event", foreign_keys=[event_uuid])

    insert_time = Column(DateTime, server_default=utcnow())

    mode = Column(String)

    owner_uuid = Column(UUID(as_uuid=True), ForeignKey("user.uuid"))

    owner = relationship("User", foreign_keys=[owner_uuid])

    queue = relationship("AlertQueue")

    queue_id = Column(UUID(as_uuid=True), ForeignKey("alert_queue.uuid"))

    tool = Column(String)

    tool_instance = Column(String)

    version = Column(UUID(as_uuid=True))

    __mapper_args__ = {
        "polymorphic_identity": "alert",
    }

    __table_args__ = (
        Index("event_uuid", event_uuid),
    )