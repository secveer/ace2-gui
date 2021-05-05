from sqlalchemy import Column, Integer, String

from db.database import Base


class ObservableType(Base):
    __tablename__ = "observable_type"

    id = Column(Integer, primary_key=True)

    value = Column(String, nullable=False, unique=True, index=True)