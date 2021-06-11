import uuid

from fastapi import status


"""
NOTE: There are no tests for the foreign key constraints, namely deleting an EventSource that is tied to an Event.
The DELETE endpoint will need to be updated once the Node endpoints are in place in order to account for this.
"""


#
# CREATE
#


def test_create_event_source(client):
    # Create an event source
    create = client.post("/api/event/source/", json={"value": "default"})
    assert create.status_code == status.HTTP_201_CREATED
    assert create.headers["Content-Location"]

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert get.status_code == status.HTTP_200_OK
    assert get.json()["description"] is None
    assert get.json()["value"] == "default"


def test_create_event_source_with_uuid(client):
    # Create an event source and specify the UUID it should use
    u = str(uuid.uuid4())
    create = client.post("/api/event/source/", json={"uuid": u, "value": "default"})
    assert create.status_code == status.HTTP_201_CREATED
    assert create.headers["Content-Location"]

    # Read it back using the UUID
    get = client.get(f"/api/event/source/{u}")
    assert get.status_code == status.HTTP_200_OK
    assert get.json()["uuid"] == u
    assert get.json()["description"] is None
    assert get.json()["value"] == "default"


def test_create_event_source_duplicate_value(client):
    # Create an event source
    client.post("/api/event/source/", json={"value": "default"})

    # Ensure you cannot create another event source with the same value
    create = client.post("/api/event/source/", json={"value": "default"})
    assert create.status_code == status.HTTP_409_CONFLICT


def test_create_event_source_invalid_uuid(client):
    create = client.post("/api/event/source/", json={"uuid": 1, "value": "default"})
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_event_source_invalid_value(client):
    create = client.post("/api/event/source/", json={"value": {"asdf": "asdf"}})
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_event_source_missing_value(client):
    create = client.post("/api/event/source/", json={})
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


#
# READ
#


def test_get_all_event_sources(client):
    # Create some event sources
    client.post("/api/event/source/", json={"value": "default"})
    client.post("/api/event/source/", json={"value": "intel"})

    # Read them back
    get = client.get("/api/event/source/")
    assert get.status_code == status.HTTP_200_OK
    assert len(get.json()) == 2


def test_get_all_event_sources_empty(client):
    get = client.get("/api/event/source/")
    assert get.status_code == status.HTTP_200_OK
    assert get.json() == []


def test_get_invalid_event_source(client):
    get = client.get("/api/event/source/1")
    assert get.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_nonexistent_event_source(client):
    get = client.get(f"/api/event/source/{uuid.uuid4()}")
    assert get.status_code == status.HTTP_404_NOT_FOUND


#
# UPDATE
#


def test_update_event_source(client):
    # Create an event source
    create = client.post("/api/event/source/", json={"value": "default"})

    # Update a single field
    update = client.put(create.headers["Content-Location"], json={"value": "test"})
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert update.headers["Content-Location"]

    # Read it back
    get = client.get(update.headers["Content-Location"])
    assert get.status_code == status.HTTP_200_OK
    assert get.json()["description"] is None
    assert get.json()["value"] == "test"


def test_update_event_source_multiple_fields(client):
    # Create an event source
    create = client.post("/api/event/source/", json={"value": "default"})

    # Update multiple fields
    update = client.put(
        create.headers["Content-Location"],
        json={"description": "Test", "value": "test"},
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert update.headers["Content-Location"]

    # Read it back
    get = client.get(update.headers["Content-Location"])
    assert get.status_code == status.HTTP_200_OK
    assert get.json()["description"] == "Test"
    assert get.json()["value"] == "test"


def test_udpate_event_source_same_value(client):
    # Create an event source
    create = client.post("/api/event/source/", json={"value": "default"})

    # Update a field to the same value
    update = client.put(create.headers["Content-Location"], json={"value": "default"})
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert update.headers["Content-Location"]

    # Read it back
    get = client.get(update.headers["Content-Location"])
    assert get.status_code == status.HTTP_200_OK
    assert get.json()["description"] is None
    assert get.json()["value"] == "default"


def test_update_event_source_duplicate_value(client):
    # Create some event sources
    client.post("/api/event/source/", json={"value": "default"})
    create = client.post("/api/event/source/", json={"value": "intel"})

    # Ensure you cannot update an event source value to one that already exists
    update = client.put(create.headers["Content-Location"], json={"value": "default"})
    assert update.status_code == status.HTTP_400_BAD_REQUEST


def test_update_event_source_invalid_uuid(client):
    update = client.put("/api/event/source/1", json={"value": "default"} )
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_event_source_invalid_value(client):
    update = client.put(f"/api/event/source/{uuid.uuid4()}", json={"value": {"asdf": "asdf"}} )
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_event_source_none_value(client):
    # Create an event source
    create = client.post("/api/event/source/", json={"value": "default"})

    # Ensure you cannot update an event source value to None
    update = client.put(create.headers["Content-Location"], json={"value": None})
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_nonexistent_event_source(client):
    update = client.put(f"/api/event/source/{uuid.uuid4()}", json={"value": "default"})
    assert update.status_code == status.HTTP_404_NOT_FOUND


#
# DELETE
#


def test_delete_event_source(client):
    # Create an event source
    create = client.post("/api/event/source/", json={"value": "default"})

    # Delete it
    delete = client.delete(create.headers["Content-Location"])
    assert delete.status_code == status.HTTP_204_NO_CONTENT

    # Make sure it is gone
    get = client.get(create.headers["Content-Location"])
    assert get.status_code == status.HTTP_404_NOT_FOUND


def test_delete_invalid_event_source(client):
    delete = client.delete("/api/event/source/1")
    assert delete.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_delete_nonexistent_event_source(client):
    delete = client.delete(f"/api/event/source/{uuid.uuid4()}")
    assert delete.status_code == status.HTTP_404_NOT_FOUND
