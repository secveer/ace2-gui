from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.database import Base
from db.schemas.helpers import utcnow


class NodeHistoryFeedback(Base):
    __tablename__ = "node_history_feedback"

    id = Column(Integer, primary_key=True)

    feedback_type = relationship("FeedbackType")

    feedback_type_id = Column(Integer, ForeignKey("feedback_type.id"))

    node_history = relationship("NodeHistory")

    node_history_id = Column(Integer, ForeignKey("node_history.id"))

    timestamp = Column(DateTime, server_default=utcnow())

    user = relationship("User")

    user_uuid = Column(UUID(as_uuid=True), ForeignKey("user.uuid"))