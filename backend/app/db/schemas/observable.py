from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Index, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from db.database import Base


class Observable(Base):
    __tablename__ = "observable"

    id = Column(Integer, primary_key=True)

    expires_on = Column(DateTime)

    for_detection = Column(Boolean, default=False)

    type = relationship("ObservableType")

    type_id = Column(Integer, ForeignKey("observable_type.id"))

    value = Column(String)

    __table_args__ = (
        Index(
            "value_trgm",
            value,
            postgresql_ops={"value": "gin_trgm_ops"},
            postgresql_using="gin",
        ),

        Index("type_value", type_id, value),

        UniqueConstraint("type_id", "value", name="type_value_uc"),
    )