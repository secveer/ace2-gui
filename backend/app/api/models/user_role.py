from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID

from api.models import type_str, validators


class UserRoleBase(BaseModel):
    """Represents a role that can be assigned to a user."""

    description: Optional[type_str] = Field(description="An optional human-readable description of the role")

    uuid: Optional[UUID] = Field(description="The UUID of the role")

    value: type_str = Field(description="The value of the role")

    _prevent_none: classmethod = validators.prevent_none("uuid", "value")


class UserRoleCreate(UserRoleBase):
    pass


class UserRoleRead(UserRoleBase):
    uuid: UUID = Field(description="The UUID of the role")

    class Config:
        orm_mode = True


class UserRoleUpdate(UserRoleBase):
    value: Optional[type_str] = Field(description="The value of the role")
