from sqlalchemy import Column, Integer, String

from db.database import Base


class EventRiskLevel(Base):
    __tablename__ = "event_risk_level"

    id = Column(Integer, primary_key=True)

    description = Column(String)

    value = Column(String, nullable=False, unique=True, index=True)