from sqlalchemy import Column, Integer, String

from db.database import Base


class FeedbackType(Base):
    __tablename__ = "feedback_type"

    id = Column(Integer, primary_key=True)

    description = Column(String)

    icon = Column(String, nullable=False, unique=True)

    value = Column(String, nullable=False, unique=True, index=True)