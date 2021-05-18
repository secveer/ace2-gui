from sqlalchemy import func, Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from db.database import Base


class Disposition(Base):
    __tablename__ = "disposition"

    uuid = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())

    description = Column(String)

    rank = Column(Integer, nullable=False, unique=True)

    value = Column(String, nullable=False, unique=True, index=True)