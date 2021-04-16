from sqlalchemy import Column, Integer, String

from db.database import Base


class Tag(Base):
    __tablename__ = "tag"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)