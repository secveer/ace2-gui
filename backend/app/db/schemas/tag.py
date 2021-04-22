from sqlalchemy import Column, Integer, String

from db.database import Base


class Tag(Base):
    __tablename__ = "tag"

    id = Column(Integer, primary_key=True)

    value = Column(String, nullable=False, unique=True, index=True)