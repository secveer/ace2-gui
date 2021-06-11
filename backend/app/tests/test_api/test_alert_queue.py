import uuid

from fastapi import status


"""
NOTE: There are no tests for the foreign key constraints, namely deleting an AlertQueue that is tied to and Alert.
The DELETE endpoint will need to be updated once the Alert endpoints are in place in order to account for this.
"""


#
# CREATE
#


def test_create_alert_queue(client):
    # Create an alert queue
    create = client.post("/api/alert/queue/", json={"value": "default"})
    assert create.status_code == status.HTTP_201_CREATED
    assert create.headers["Content-Location"]

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert get.status_code == status.HTTP_200_OK
    assert get.json()["description"] is None
    assert get.json()["value"] == "default"


def test_create_alert_queue_with_uuid(client):
    # Create an alert queue and specify the UUID it should use
    u = str(uuid.uuid4())
    create = client.post("/api/alert/queue/", json={"uuid": u, "value": "default"})
    assert create.status_code == status.HTTP_201_CREATED
    assert create.headers["Content-Location"]

    # Read it back using the UUID
    get = client.get(f"/api/alert/queue/{u}")
    assert get.status_code == status.HTTP_200_OK
    assert get.json()["uuid"] == u
    assert get.json()["description"] is None
    assert get.json()["value"] == "default"


def test_create_alert_queue_duplicate_value(client):
    # Create an alert queue
    client.post("/api/alert/queue/", json={"value": "default"})

    # Ensure you cannot create another alert_queue with the same value
    create = client.post("/api/alert/queue/", json={"value": "default"})
    assert create.status_code == status.HTTP_409_CONFLICT


def test_create_alert_queue_invalid_uuid(client):
    create = client.post("/api/alert/queue/", json={"uuid": 1, "value": "default"})
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_alert_queue_invalid_value(client):
    create = client.post("/api/alert/queue/", json={"value": {"asdf": "asdf"}})
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_alert_queue_missing_value(client):
    create = client.post("/api/alert/queue/", json={})
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


#
# READ
#


def test_get_all_alert_queues(client):
    # Create some alert queues
    client.post("/api/alert/queue/", json={"value": "default"})
    client.post("/api/alert/queue/", json={"value": "intel"})
    
    # Read them back
    get = client.get("/api/alert/queue/")
    assert get.status_code == status.HTTP_200_OK
    assert len(get.json()) == 2


def test_get_all_alert_queues_empty(client):
    get = client.get("/api/alert/queue/")
    assert get.status_code == status.HTTP_200_OK
    assert get.json() == []


def test_get_invalid_alert_queue(client):
    get = client.get("/api/alert/queue/1")
    assert get.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_nonexistent_alert_queue(client):
    get = client.get(f"/api/alert/queue/{uuid.uuid4()}")
    assert get.status_code == status.HTTP_404_NOT_FOUND


#
# UPDATE
#


def test_update_alert_queue(client):
    # Create an alert queue
    create = client.post("/api/alert/queue/", json={"value": "default"})

    # Update a single field
    update = client.put(create.headers["Content-Location"], json={"value": "test"})
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert update.headers["Content-Location"]

    # Read it back
    get = client.get(update.headers["Content-Location"])
    assert get.status_code == status.HTTP_200_OK
    assert get.json()["description"] is None
    assert get.json()["value"] == "test"


def test_update_alert_queue_multiple_fields(client):
    # Create an alert queue
    create = client.post("/api/alert/queue/", json={"value": "default"})

    # Update multiple fields
    update = client.put(create.headers["Content-Location"], json={"description": "Test", "value": "test"})
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert update.headers["Content-Location"]

    # Read it back
    get = client.get(update.headers["Content-Location"])
    assert get.status_code == status.HTTP_200_OK
    assert get.json()["description"] == "Test"
    assert get.json()["value"] == "test"


def test_udpate_alert_queue_same_value(client):
    # Create an alert queue
    create = client.post("/api/alert/queue/", json={"value": "default"})

    # Update a field to the same value
    update = client.put(create.headers["Content-Location"], json={"value": "default"})
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert update.headers["Content-Location"]

    # Read it back
    get = client.get(update.headers["Content-Location"])
    assert get.status_code == status.HTTP_200_OK
    assert get.json()["description"] is None
    assert get.json()["value"] == "default"


def test_update_alert_queue_duplicate_value(client):
    # Create some alert_queues
    client.post("/api/alert/queue/", json={"value": "default"})
    create = client.post("/api/alert/queue/", json={"value": "intel"})

    # Ensure you cannot update an alert queue value to one that already exists
    update = client.put(create.headers["Content-Location"], json={"value": "default"})
    assert update.status_code == status.HTTP_400_BAD_REQUEST


def test_update_alert_queue_invalid_uuid(client):
    update = client.put("/api/alert/queue/1", json={"value": "default"})
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_alert_queue_invalid_value(client):
    # Ensure you cannot update a value to an invalid value
    update = client.put(f"/api/alert/queue/{uuid.uuid4()}", json={"value": {"asdf": "asdf"}})
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_alert_queue_none_value(client):
    # Create an alert queue
    create = client.post("/api/alert/queue/", json={"value": "default"})

    # Ensure you cannot update an alert_queue value to None
    update = client.put(create.headers["Content-Location"], json={"value": None})
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_nonexistent_alert_queue(client):
    update = client.put(f"/api/alert/queue/{uuid.uuid4()}", json={"value": "default"})
    assert update.status_code == status.HTTP_404_NOT_FOUND


#
# DELETE
#


def test_delete_alert_queue(client):
    # Create an alert queue
    create = client.post("/api/alert/queue/", json={"value": "default"})

    # Delete it
    delete = client.delete(create.headers["Content-Location"])
    assert delete.status_code == status.HTTP_204_NO_CONTENT

    # Make sure it is gone
    get = client.get(create.headers["Content-Location"])
    assert get.status_code == status.HTTP_404_NOT_FOUND


def test_delete_invalid_alert_queue(client):
    delete = client.delete("/api/alert/queue/1")
    assert delete.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_delete_nonexistent_alert_queue(client):
    delete = client.delete(f"/api/alert/queue/{uuid.uuid4()}")
    assert delete.status_code == status.HTTP_404_NOT_FOUND