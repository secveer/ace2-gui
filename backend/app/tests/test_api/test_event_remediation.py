import uuid


"""
NOTE: There are no tests for the foreign key constraints, namely deleting an EventRemediation that is tied to an Event.
The DELETE endpoint will need to be updated once the Node endpoints are in place in order to account for this.
"""


#
# CREATE
#


def test_create_event_remediation(client):
    # Create an event remediation
    create = client.post("/api/event/remediation/", json={"value": "default"})
    assert create.status_code == 201
    assert create.headers["Content-Location"]

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert get.status_code == 200
    assert get.json()["description"] is None
    assert get.json()["value"] == "default"


def test_create_event_remediation_with_uuid(client):
    # Create an event remediation and specify the UUID it should use
    u = str(uuid.uuid4())
    create = client.post("/api/event/remediation/", json={"uuid": u, "value": "default"})
    assert create.status_code == 201
    assert create.headers["Content-Location"]

    # Read it back using the UUID
    get = client.get(f"/api/event/remediation/{u}")
    assert get.status_code == 200
    assert get.json()["uuid"] == u
    assert get.json()["description"] is None
    assert get.json()["value"] == "default"


def test_create_event_remediation_duplicate_value(client):
    # Create an event remediation
    client.post("/api/event/remediation/", json={"value": "default"})

    # Ensure you cannot create another event remediation with the same value
    create = client.post("/api/event/remediation/", json={"value": "default"})
    assert create.status_code == 409


def test_create_event_remediation_invalid_uuid(client):
    create = client.post("/api/event/remediation/", json={"uuid": 1, "value": "default"})
    assert create.status_code == 422


def test_create_event_remediation_invalid_value(client):
    create = client.post("/api/event/remediation/", json={"value": {"asdf": "asdf"}})
    assert create.status_code == 422


def test_create_event_remediation_missing_value(client):
    create = client.post("/api/event/remediation/", json={})
    assert create.status_code == 422


#
# READ
#


def test_get_all_event_remediations(client):
    # Create some event remediations
    client.post("/api/event/remediation/", json={"value": "default"})
    client.post("/api/event/remediation/", json={"value": "intel"})

    # Read them back
    get = client.get("/api/event/remediation/")
    assert get.status_code == 200
    assert len(get.json()) == 2


def test_get_all_event_remediations_empty(client):
    get = client.get("/api/event/remediation/")
    assert get.status_code == 200
    assert get.json() == []


def test_get_invalid_event_remediation(client):
    get = client.get("/api/event/remediation/1")
    assert get.status_code == 422


def test_get_nonexistent_event_remediation(client):
    get = client.get(f"/api/event/remediation/{uuid.uuid4()}")
    assert get.status_code == 404


#
# UPDATE
#


def test_update_event_remediation(client):
    # Create an event remediation
    create = client.post("/api/event/remediation/", json={"value": "default"})

    # Update a single field
    update = client.put(create.headers["Content-Location"], json={"value": "test"})
    assert update.status_code == 204
    assert update.headers["Content-Location"]

    # Read it back
    get = client.get(update.headers["Content-Location"])
    assert get.status_code == 200
    assert get.json()["description"] is None
    assert get.json()["value"] == "test"


def test_update_event_remediation_multiple_fields(client):
    # Create an event remediation
    create = client.post("/api/event/remediation/", json={"value": "default"})

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


def test_udpate_event_remediation_same_value(client):
    # Create an event remediation
    create = client.post("/api/event/remediation/", json={"value": "default"})

    # Update a field to the same value
    update = client.put(create.headers["Content-Location"], json={"value": "default"})
    assert update.status_code == 204
    assert update.headers["Content-Location"]

    # Read it back
    get = client.get(update.headers["Content-Location"])
    assert get.status_code == 200
    assert get.json()["description"] is None
    assert get.json()["value"] == "default"


def test_update_event_remediation_duplicate_value(client):
    # Create some event remediations
    client.post("/api/event/remediation/", json={"value": "default"})
    create = client.post("/api/event/remediation/", json={"value": "intel"})

    # Ensure you cannot update an event remediation value to one that already exists
    update = client.put(create.headers["Content-Location"], json={"value": "default"})
    assert update.status_code == 400


def test_update_event_remediation_invalid_uuid(client):
    update = client.put("/api/event/remediation/1", json={"value": "default"})
    assert update.status_code == 422


def test_update_event_remediation_invalid_value(client):
    update = client.put(f"/api/event/remediation/{uuid.uuid4()}", json={"value": {"asdf": "asdf"}})
    assert update.status_code == 422


def test_update_event_remediation_none_value(client):
    # Create an event remediation
    create = client.post("/api/event/remediation/", json={"value": "default"})

    # Ensure you cannot update an event remediation value to None
    update = client.put(create.headers["Content-Location"], json={"value": None})
    assert update.status_code == 422


def test_update_nonexistent_event_remediation(client):
    update = client.put(f"/api/event/remediation/{uuid.uuid4()}", json={"value": "default"})
    assert update.status_code == 404


#
# DELETE
#


def test_delete_event_remediation(client):
    # Create an event remediation
    create = client.post("/api/event/remediation/", json={"value": "default"})

    # Delete it
    delete = client.delete(create.headers["Content-Location"])
    assert delete.status_code == 204

    # Make sure it is gone
    get = client.get(create.headers["Content-Location"])
    assert get.status_code == 404


def test_delete_invalid_event_remediation(client):
    delete = client.delete("/api/event/remediation/1")
    assert delete.status_code == 422


def test_delete_nonexistent_event_remediation(client):
    delete = client.delete(f"/api/event/remediation/{uuid.uuid4()}")
    assert delete.status_code == 404
