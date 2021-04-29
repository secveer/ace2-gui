from sqlalchemy import Column, Integer, String

from db.database import Base


class Disposition(Base):
    __tablename__ = "disposition"

    id = Column(Integer, primary_key=True)

    description = Column(String)

    rank = Column(Integer, nullable=False, unique=True)

    value = Column(String, nullable=False, unique=True, index=True)