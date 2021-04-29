from sqlalchemy import Column, Integer, String

from db.database import Base


class NodeHistoryAction(Base):
    __tablename__ = "node_history_action"

    id = Column(Integer, primary_key=True)

    value = Column(String, nullable=False, unique=True, index=True)