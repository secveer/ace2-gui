from sqlalchemy import Column, Integer, String

from db.database import Base


class Directive(Base):
    __tablename__ = "directive"

    id = Column(Integer, primary_key=True)

    description = Column(String)

    value = Column(String, nullable=False, unique=True, index=True)