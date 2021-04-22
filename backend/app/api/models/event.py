from datetime import datetime
from pydantic import Field
from typing import List, Optional

from api.models.alert import Alert
from api.models.node import Node
from api.models.event_prevention_tool import EventPreventionTool
from api.models.event_remediation import EventRemediation
from api.models.event_status import EventStatus
from api.models.event_type import EventType
from api.models.event_vector import EventVector


class Event(Node):
    """Represents a collection of alerts that combine to form an attack."""

    alert_time: Optional[datetime] = Field(description="The time of the earliest alert in the event")

    alerts: Optional[List[Alert]] = Field(description="A list of alerts contained in the event")

    contain_time: Optional[datetime] = Field(description="The time the attack represented by the event was contained")

    creation_time: datetime = Field(description="The time the event was created")

    disposition_time: Optional[datetime] = Field(description="The earliest time one of the alerts in the event was dispositioned")

    event_time: Optional[datetime] = Field(description="The time at which the attack represented by the event occurred")

    name: str = Field(description="The name of the event")

    ownership_time: Optional[datetime] = Field(description="The earliest time an analyst took ownership over an alert in the event")

    prevention_tools: Optional[List[EventPreventionTool]] = Field(description="A list of prevention tools involved in the event")

    remediation_time: Optional[datetime] = Field(description="The earliest time that any remediation was performed on the attack represented by the event")

    remediations: Optional[List[EventRemediation]] = Field(description="A list of remediations performed to clean up the attack represented by the event")

    risk_level: Optional[str] = Field(description="The risk level assigned to the event")

    status: EventStatus = Field(description="The status assigned to the event")

    type: Optional[EventType] = Field(description="The type assigned to the event")

    vectors: Optional[List[EventVector]] = Field(description="A list of vectors assigned to the event")

    class Config:
        orm_mode = True