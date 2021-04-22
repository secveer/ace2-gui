from datetime import datetime
from pydantic import Field, UUID4
from typing import List, Optional

from api.models.analysis import Analysis
from api.models.node import Node
from api.models.observable import Observable


class ObservableInstance(Node):
    """Represents an individual observable inside of an analysis."""

    alert_uuid: UUID4 = Field(description="The unique ID of the alert containing this observable")

    analysis: Optional[List[Analysis]] = Field(description="A list of analyses performed on this observable instance")

    observable: Observable = Field(description="The observable represented by this instance")

    redirection: Optional["ObservableInstance"] = Field(description="An optional field denoting another observable instance to which this one should point")

    time: datetime = Field(description="The time this observable instance was observed")

    class Config:
        orm_mode = True