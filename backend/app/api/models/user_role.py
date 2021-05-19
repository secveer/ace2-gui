from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID


class UserRoleBase(BaseModel):
    """Represents a role that can be assigned to a user."""

    description: Optional[str] = Field(description="An optional human-readable description of the role")

    uuid: Optional[UUID] = Field(description="The UUID of the role")

    value: str = Field(description="The value of the role")


class UserRoleCreate(UserRoleBase):
    pass


class UserRoleRead(UserRoleBase):
    uuid: UUID = Field(description="The UUID of the role")

    class Config:
        orm_mode = True


class UserRoleUpdate(UserRoleBase):
    value: Optional[str] = Field(description="The value of the role")