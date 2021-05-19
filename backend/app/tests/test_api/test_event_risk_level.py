import uuid


"""
NOTE: There are no tests for the foreign key constraints, namely deleting an EventRiskLevel that is tied to an Event.
The DELETE endpoint will need to be updated once the Node endpoints are in place in order to account for this.
"""


#
# CREATE
#


def test_create_event_risk_level(client):
    # Create an event risk level
    create = client.post("/api/event/risk_level", json={"value": "default"})
    assert create.status_code == 201
    assert create.headers["Content-Location"]

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert get.status_code == 200
    assert get.json()["description"] is None
    assert get.json()["value"] == "default"


def test_create_event_risk_level_with_uuid(client):
    # Create an event risk level and specify the UUID it should use
    u = str(uuid.uuid4())
    create = client.post("/api/event/risk_level", json={"uuid": u, "value": "default"})
    assert create.status_code == 201
    assert create.headers["Content-Location"]

    # Read it back using the UUID
    get = client.get(f"/api/event/risk_level/{u}")
    assert get.status_code == 200
    assert get.json()["uuid"] == u
    assert get.json()["description"] is None
    assert get.json()["value"] == "default"


def test_create_event_risk_level_duplicate_value(client):
    # Create an event risk level
    client.post("/api/event/risk_level", json={"value": "default"})

    # Ensure you cannot create another event risk level with the same value
    create = client.post("/api/event/risk_level", json={"value": "default"})
    assert create.status_code == 409


def test_create_event_risk_level_invalid_value(client):
    create = client.post("/api/event/risk_level", json={"value": {"asdf": "asdf"}})
    assert create.status_code == 422


def test_create_event_risk_level_missing_value(client):
    create = client.post("/api/event/risk_level", json={})
    assert create.status_code == 422


#
# READ
#


def test_get_all_event_risk_levels(client):
    # Create some event risk levels
    client.post("/api/event/risk_level", json={"value": "default"})
    client.post("/api/event/risk_level", json={"value": "intel"})

    # Read them back
    get = client.get("/api/event/risk_level")
    assert get.status_code == 200
    assert len(get.json()) == 2


def test_get_all_event_risk_levels_empty(client):
    get = client.get("/api/event/risk_level")
    assert get.status_code == 200
    assert get.json() == []


def test_get_nonexistent_event_risk_level(client):
    get = client.get(f"/api/event/risk_level/{uuid.uuid4()}")
    assert get.status_code == 404


#
# UPDATE
#


def test_update_event_risk_level(client):
    # Create an event risk level
    create = client.post("/api/event/risk_level", json={"value": "default"})

    # Update a single field
    update = client.put(create.headers["Content-Location"], json={"value": "test"})
    assert update.status_code == 204
    assert update.headers["Content-Location"]

    # Read it back
    get = client.get(update.headers["Content-Location"])
    assert get.status_code == 200
    assert get.json()["description"] is None
    assert get.json()["value"] == "test"


def test_update_event_risk_level_multiple_fields(client):
    # Create an event risk level
    create = client.post("/api/event/risk_level", json={"value": "default"})

    # Update multiple fields
    update = client.put(
        create.headers["Content-Location"],
        json={"description": "Test", "value": "test"},
    )
    assert update.status_code == 204
    assert update.headers["Content-Location"]

    # Read it back
    get = client.get(update.headers["Content-Location"])
    assert get.status_code == 200
    assert get.json()["description"] == "Test"
    assert get.json()["value"] == "test"


def test_udpate_event_risk_level_same_value(client):
    # Create an event risk level
    create = client.post("/api/event/risk_level", json={"value": "default"})

    # Update a field to the same value
    update = client.put(create.headers["Content-Location"], json={"value": "default"})
    assert update.status_code == 204
    assert update.headers["Content-Location"]

    # Read it back
    get = client.get(update.headers["Content-Location"])
    assert get.status_code == 200
    assert get.json()["description"] is None
    assert get.json()["value"] == "default"


def test_update_event_risk_level_duplicate_value(client):
    # Create some event risk levels
    client.post("/api/event/risk_level", json={"value": "default"})
    create = client.post("/api/event/risk_level", json={"value": "intel"})

    # Ensure you cannot update an event risk level value to one that already exists
    update = client.put(create.headers["Content-Location"], json={"value": "default"})
    assert update.status_code == 400


def test_update_event_risk_level_invalid_value(client):
    # Create an event risk level
    create = client.post("/api/event/risk_level", json={"value": "default"})

    # Ensure you cannot update a value to an invalid value
    update = client.put(
        create.headers["Content-Location"], json={"value": {"asdf": "asdf"}}
    )
    assert update.status_code == 422


def test_update_event_risk_level_none_value(client):
    # Create an event risk level
    create = client.post("/api/event/risk_level", json={"value": "default"})

    # Ensure you cannot update an event risk level value to None
    update = client.put(create.headers["Content-Location"], json={"value": None})
    assert update.status_code == 400


def test_update_nonexistent_event_risk_level(client):
    update = client.put(f"/api/event/risk_level/{uuid.uuid4()}", json={"value": "default"})
    assert update.status_code == 404


#
# DELETE
#


def test_delete_event_risk_level(client):
    # Create an event risk level
    create = client.post("/api/event/risk_level", json={"value": "default"})

    # Delete it
    delete = client.delete(create.headers["Content-Location"])
    assert delete.status_code == 204

    # Make sure it is gone
    get = client.get(create.headers["Content-Location"])
    assert get.status_code == 404


def test_delete_nonexistent_event_risk_level(client):
    delete = client.delete(f"/api/event/risk_level/{uuid.uuid4()}")
    assert delete.status_code == 400
