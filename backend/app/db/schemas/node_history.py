from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from db.database import Base
from db.schemas.helpers import utcnow


class NodeHistory(Base):
    __tablename__ = "node_history"

    id = Column(Integer, primary_key=True)

    action = relationship("NodeHistoryAction")

    action_id = Column(Integer, ForeignKey("node_history_action.id"))

    action_user_uuid = Column(UUID(as_uuid=True), ForeignKey("user.uuid"))

    action_user = relationship("User", foreign_keys=[action_user_uuid])

    after = Column(JSONB)

    before = Column(JSONB)

    feedback = relationship("NodeHistoryFeedback")

    node_uuid = Column(UUID(as_uuid=True), ForeignKey("node.uuid"))

    node = relationship("Node", foreign_keys=[node_uuid])

    timestamp = Column(DateTime, server_default=utcnow())