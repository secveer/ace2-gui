from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID, uuid4

from api.models import type_str, validators


class UserRoleBase(BaseModel):
    """Represents a role that can be assigned to a user."""

    description: Optional[type_str] = Field(description="An optional human-readable description of the role")

    uuid: UUID = Field(default_factory=uuid4, description="The UUID of the role")

    value: type_str = Field(description="The value of the role")


class UserRoleCreate(UserRoleBase):
    pass


class UserRoleRead(UserRoleBase):
    class Config:
        orm_mode = True


class UserRoleUpdate(UserRoleBase):
    value: Optional[type_str] = Field(description="The value of the role")

    _prevent_none: classmethod = validators.prevent_none("value")
