from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.schemas.node import Node
from db.schemas.user_role_mapping import user_role_mapping


class User(Node):
    __tablename__ = "user"

    uuid = Column(UUID(as_uuid=True), ForeignKey("node.uuid"), primary_key=True)

    api_key = Column(String, unique=True)

    default_queue = relationship("AlertQueue")

    default_queue_id = Column(Integer, ForeignKey("alert_queue.id"))

    display_name = Column(String)

    email = Column(String, unique=True)

    enabled = Column(Boolean, default=True)

    password = Column(String)

    roles = relationship("Role", secondary=user_role_mapping)

    salt = Column(String)

    timezone = Column(String, default="UTC")

    username = Column(String, unique=True)

    __mapper_args__ = {
        "polymorphic_identity": "user",
    }