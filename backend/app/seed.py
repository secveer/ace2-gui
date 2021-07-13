import os
import sys
import yaml

from sqlalchemy.orm import Session

from db import crud
from db.database import get_db
from db.schemas.alert_disposition import AlertDisposition
from db.schemas.alert_queue import AlertQueue
from db.schemas.alert_type import AlertType
from db.schemas.event_prevention_tool import EventPreventionTool
from db.schemas.event_remediation import EventRemediation
from db.schemas.event_risk_level import EventRiskLevel
from db.schemas.event_source import EventSource
from db.schemas.event_status import EventStatus
from db.schemas.event_type import EventType
from db.schemas.event_vector import EventVector
from db.schemas.node_threat_type import NodeThreatType
from db.schemas.user import User
from db.schemas.user_role import UserRole


# Quit early if the config file does not exist
if not os.path.exists("etc/defaults.yml"):
    print("etc/defaults.yml does not exist!")
    sys.exit()

data = None
with open("etc/defaults.yml", "r") as yamlfile:
    data = yaml.load(yamlfile, Loader=yaml.FullLoader)

# Quit early if the config file is empty
if data is None:
    print("etc/defaults.yml is empty!")
    sys.exit()

# Get a database connection
db: Session = next(get_db())

# Add the objects to the database
if "alert_disposition" in data:
    for rank, value in enumerate(data["alert_disposition"]):
        db.add(AlertDisposition(rank=rank, value=value))
        print(f"Adding alert disposition: {rank}:{value}")

if "alert_queue" in data:
    # Make sure there is always a "default" queue
    if "default" not in data["alert_queue"]:
        data["alert_queue"].append("default")

    for value in data["alert_queue"]:
        db.add(AlertQueue(value=value))
        print(f"Adding alert queue: {value}")
else:
    # Make sure there is always a "default" queue
    db.add(AlertQueue(value="default"))
    print("Adding alert queue: default")

if "alert_type" in data:
    for value in data["alert_type"]:
        db.add(AlertType(value=value))
        print(f"Adding alert type: {value}")

if "event_prevention_tool" in data:
    for value in data["event_prevention_tool"]:
        db.add(EventPreventionTool(value=value))
        print(f"Adding event prevention tool: {value}")

if "event_remediation" in data:
    for value in data["event_remediation"]:
        db.add(EventRemediation(value=value))
        print(f"Adding event remediation: {value}")

if "event_risk_level" in data:
    for value in data["event_risk_level"]:
        db.add(EventRiskLevel(value=value))
        print(f"Adding event risk level: {value}")

if "event_source" in data:
    for value in data["event_source"]:
        db.add(EventSource(value=value))
        print(f"Adding event source: {value}")

if "event_status" in data:
    for value in data["event_status"]:
        db.add(EventStatus(value=value))
        print(f"Adding event status: {value}")

if "event_type" in data:
    for value in data["event_type"]:
        db.add(EventType(value=value))
        print(f"Adding event type: {value}")

if "event_vector" in data:
    for value in data["event_vector"]:
        db.add(EventVector(value=value))
        print(f"Adding event vector: {value}")

if "node_threat_type" in data:
    for value in data["node_threat_type"]:
        db.add(NodeThreatType(value=value))
        print(f"Adding node threat type: {value}")

if "user_role" in data:
    # Make sure there is always an "admin" role
    if "admin" not in data["user_role"]:
        data["user_role"].append("admin")

    for value in data["user_role"]:
        db.add(UserRole(value=value))
        print(f"Adding user role: {value}")
else:
    # Make sure there is always an "admin" role
    db.add(UserRole(value="admin"))
    print("Adding user role: admin")

# Commit the database changes so that they can be used to create the analyst user
crud.commit(db)

# Add an "analyst" user
db.add(User(
    default_alert_queue=crud.read_by_value(value="default", db_table=AlertQueue, db=db),
    display_name="Analyst",
    email="analyst@localhost",
    password="analyst",
    roles=crud.read_by_values(values=["admin"], db_table=UserRole, db=db),
    username="analyst",
))
print("Adding user: analyst")

# Commit all of the changes
crud.commit(db)
