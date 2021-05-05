from datetime import datetime
from pydantic import Field, UUID4
from typing import Optional

from api.models.alert_queue import AlertQueue
from api.models.alert_type import AlertType
from api.models.analysis import Analysis
from api.models.disposition import Disposition
from api.models.user import User


class Alert(Analysis):
    """Represents a RootAnalysis from the core that has at least one detection point."""

    alert_type: AlertType = Field(description="The type of this alert")

    disposition: Optional[Disposition] = Field(description="The disposition assigned to this alert")

    disposition_time: Optional[datetime] = Field(description="The time this alert was most recently dispositioned")

    disposition_user: Optional[User] = Field(description="The user who most recently dispositioned this alert")

    event_uuid: Optional[UUID4] = Field(description="The unique ID of the event containing this alert")

    insert_time: datetime = Field(description="The time this alert was created")

    mode: str = Field(description="The mode under which this alert is currently operating")

    owner: Optional[User] = Field(description="The user who has taken ownership of this alert")

    queue: AlertQueue = Field(description="The alert queue containing this alert")

    tool: str = Field(description="The tool that created this alert")

    tool_instance: str = Field(description="The instance of the tool that created this alert")

    version: UUID4 = Field(description="The version of this alert")

    class Config:
        orm_mode = True