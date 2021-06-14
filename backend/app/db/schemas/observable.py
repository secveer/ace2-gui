from sqlalchemy import (
    func,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Index,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.database import Base


class Observable(Base):
    __tablename__ = "observable"

    uuid = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())

    expires_on = Column(DateTime)

    for_detection = Column(Boolean, default=False)

    type = relationship("ObservableType")

    type_uuid = Column(UUID(as_uuid=True), ForeignKey("observable_type.uuid"))

    value = Column(String)

    __table_args__ = (
        Index(
            "value_trgm",
            value,
            postgresql_ops={"value": "gin_trgm_ops"},
            postgresql_using="gin",
        ),
        Index("type_value", type_uuid, value),
        UniqueConstraint("type_uuid", "value", name="type_value_uc"),
    )
