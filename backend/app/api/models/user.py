from pydantic import Field
from typing import List

from api.models.node import Node


class User(Node):
    """Represents a user account within the application."""

    default_queue: str = Field(description="The default alert queue the user will see on the alert management page")

    display_name: str = Field(description="The user's full name")

    email: str = Field(description="The user's email address")

    enabled: bool = Field(description="Whether or not the user account is enabled and can access the application")

    roles: List[str] = Field(description="A list of roles assigned to the user")

    timezone: str = Field(
        description="The timezone that will be used when the user views timestamps in the application"
    )

    username: str = Field(description="The username used to sign into the application")

    class Config:
        orm_mode = True
