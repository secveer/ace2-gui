from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from db.database import Base
from db.schemas.threat_threat_type_mapping import threat_threat_type_mapping


class Threat(Base):
    __tablename__ = "threat"

    id = Column(Integer, primary_key=True)

    description = Column(String)

    types = relationship("ThreatType", secondary=threat_threat_type_mapping)

    value = Column(String, nullable=False, unique=True, index=True)