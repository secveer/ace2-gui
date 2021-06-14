from sqlalchemy import func, Column, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.database import Base
from db.schemas.helpers import utcnow


class NodeHistoryFeedback(Base):
    __tablename__ = "node_history_feedback"

    uuid = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())

    feedback_type = relationship("FeedbackType")

    feedback_type_uuid = Column(UUID(as_uuid=True), ForeignKey("feedback_type.uuid"))

    node_history = relationship("NodeHistory")

    node_history_uuid = Column(UUID(as_uuid=True), ForeignKey("node_history.uuid"))

    timestamp = Column(DateTime, server_default=utcnow())

    user = relationship("User")

    user_uuid = Column(UUID(as_uuid=True), ForeignKey("user.uuid"))
