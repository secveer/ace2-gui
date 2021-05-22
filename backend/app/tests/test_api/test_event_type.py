import uuid


"""
NOTE: There are no tests for the foreign key constraints, namely deleting an EventType that is tied to an Event.
The DELETE endpoint will need to be updated once the Node endpoints are in place in order to account for this.
"""


#
# CREATE
#


def test_create_event_type(client):
    # Create an event type
    create = client.post("/api/event/type/", json={"value": "default"})
    assert create.status_code == 201
    assert create.headers["Content-Location"]

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert get.status_code == 200
    assert get.json()["description"] is None
    assert get.json()["value"] == "default"


def test_create_event_type_with_uuid(client):
    # Create an event type and specify the UUID it should use
    u = str(uuid.uuid4())
    create = client.post("/api/event/type/", json={"uuid": u, "value": "default"})
    assert create.status_code == 201
    assert create.headers["Content-Location"]

    # Read it back using the UUID
    get = client.get(f"/api/event/type/{u}")
    assert get.status_code == 200
    assert get.json()["uuid"] == u
    assert get.json()["description"] is None
    assert get.json()["value"] == "default"


def test_create_event_type_duplicate_value(client):
    # Create an event type
    client.post("/api/event/type/", json={"value": "default"})

    # Ensure you cannot create another event type with the same value
    create = client.post("/api/event/type/", json={"value": "default"})
    assert create.status_code == 409


def test_create_event_type_invalid_value(client):
    create = client.post("/api/event/type/", json={"value": {"asdf": "asdf"}})
    assert create.status_code == 422


def test_create_event_type_missing_value(client):
    create = client.post("/api/event/type/", json={})
    assert create.status_code == 422


#
# READ
#


def test_get_all_event_types(client):
    # Create some event types
    client.post("/api/event/type/", json={"value": "default"})
    client.post("/api/event/type/", json={"value": "intel"})

    # Read them back
    get = client.get("/api/event/type/")
    assert get.status_code == 200
    assert len(get.json()) == 2


def test_get_all_event_types_empty(client):
    get = client.get("/api/event/type/")
    assert get.status_code == 200
    assert get.json() == []


def test_get_invalid_event_type(client):
    get = client.get("/api/event/type/1")
    assert get.status_code == 422


def test_get_nonexistent_event_type(client):
    get = client.get(f"/api/event/type/{uuid.uuid4()}")
    assert get.status_code == 404


#
# UPDATE
#


def test_update_event_type(client):
    # Create an event type
    create = client.post("/api/event/type/", json={"value": "default"})

    # Update a single field
    update = client.put(create.headers["Content-Location"], json={"value": "test"})
    assert update.status_code == 204
    assert update.headers["Content-Location"]

    # Read it back
    get = client.get(update.headers["Content-Location"])
    assert get.status_code == 200
    assert get.json()["description"] is None
    assert get.json()["value"] == "test"


def test_update_event_type_multiple_fields(client):
    # Create an event type
    create = client.post("/api/event/type/", json={"value": "default"})

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


def test_udpate_event_type_same_value(client):
    # Create an event type
    create = client.post("/api/event/type/", json={"value": "default"})

    # Update a field to the same value
    update = client.put(create.headers["Content-Location"], json={"value": "default"})
    assert update.status_code == 204
    assert update.headers["Content-Location"]

    # Read it back
    get = client.get(update.headers["Content-Location"])
    assert get.status_code == 200
    assert get.json()["description"] is None
    assert get.json()["value"] == "default"


def test_update_event_type_duplicate_value(client):
    # Create some event types
    client.post("/api/event/type/", json={"value": "default"})
    create = client.post("/api/event/type/", json={"value": "intel"})

    # Ensure you cannot update an event type value to one that already exists
    update = client.put(create.headers["Content-Location"], json={"value": "default"})
    assert update.status_code == 400


def test_update_event_type_invalid_value(client):
    # Create an event type
    create = client.post("/api/event/type/", json={"value": "default"})

    # Ensure you cannot update a value to an invalid value
    update = client.put(
        create.headers["Content-Location"], json={"value": {"asdf": "asdf"}}
    )
    assert update.status_code == 422


def test_update_event_type_none_value(client):
    # Create an event type
    create = client.post("/api/event/type/", json={"value": "default"})

    # Ensure you cannot update an event type value to None
    update = client.put(create.headers["Content-Location"], json={"value": None})
    assert update.status_code == 400


def test_update_nonexistent_event_type(client):
    update = client.put(f"/api/event/type/{uuid.uuid4()}", json={"value": "default"})
    assert update.status_code == 404


#
# DELETE
#


def test_delete_event_type(client):
    # Create an event type
    create = client.post("/api/event/type/", json={"value": "default"})

    # Delete it
    delete = client.delete(create.headers["Content-Location"])
    assert delete.status_code == 204

    # Make sure it is gone
    get = client.get(create.headers["Content-Location"])
    assert get.status_code == 404


def test_delete_nonexistent_event_type(client):
    delete = client.delete(f"/api/event/type/{uuid.uuid4()}")
    assert delete.status_code == 400
