from sqlalchemy import Column, Integer, String

from db.database import Base


class EventVector(Base):
    __tablename__ = "event_vector"

    id = Column(Integer, primary_key=True)

    description = Column(String)

    value = Column(String, nullable=False, unique=True, index=True)