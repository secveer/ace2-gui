from pydantic import BaseModel, Field, UUID4
from typing import List, Optional

from api.models.comment import Comment
from api.models.directive import Directive
from api.models.tag import Tag
from api.models.threat import Threat
from api.models.threat_actor import ThreatActor


class Node(BaseModel):
    """Represents an individual node."""

    comments: Optional[List[Comment]] = Field(description="A list of comments added to the node")

    directives: Optional[List[Directive]] = Field(description="A list of directives applied to the node")

    tags: Optional[List[Tag]] = Field(description="A list of tags assigned to the node")

    threat_actor: Optional[ThreatActor] = Field(description="The threat actor assigned to the node")

    threats: Optional[List[Threat]] = Field(description="A list of threats assigned to the node")

    uuid: UUID4 = Field(description="The unique ID of the analysis")

    class Config:
        orm_mode = True
