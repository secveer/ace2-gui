from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.schemas.analysis_observable_instance_mapping import analysis_observable_instance_mapping
from db.schemas.helpers import utcnow
from db.schemas.node import Node


class ObservableInstance(Node):
    __tablename__ = "observable_instance"

    uuid = Column(UUID(as_uuid=True), ForeignKey("node.uuid"), primary_key=True)

    alert_uuid = Column(UUID(as_uuid=True), ForeignKey("alert.uuid"))

    analysis = relationship("Analysis", secondary=analysis_observable_instance_mapping)

    observable = relationship("Observable")

    observable_uuid = Column(UUID(as_uuid=True), ForeignKey("observable.uuid"))

    redirection = Column(UUID(as_uuid=True), ForeignKey("observable_instance.uuid"))

    time = Column(DateTime, server_default=utcnow())

    __mapper_args__ = {
        "polymorphic_identity": "observable_instance",
    }