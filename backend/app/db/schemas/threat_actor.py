from sqlalchemy import Column, Integer, String

from db.database import Base


class ThreatActor(Base):
    __tablename__ = "threat_actor"

    id = Column(Integer, primary_key=True)

    description = Column(String)

    value = Column(String, nullable=False, unique=True, index=True)