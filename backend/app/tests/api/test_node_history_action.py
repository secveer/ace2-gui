import uuid

from fastapi import status


"""
NOTE: There are no tests for the foreign key constraints, namely deleting an NodeHistoryAction that is tied to a Node.
The DELETE endpoint will need to be updated once the Node endpoints are in place in order to account for this.
"""


#
# CREATE
#


def test_create_node_history_action(client):
    # Create a node history action
    create = client.post("/api/node/history/action/", json={"value": "default"})
    assert create.status_code == status.HTTP_201_CREATED
    assert create.headers["Content-Location"]

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert get.status_code == status.HTTP_200_OK
    assert get.json()["description"] is None
    assert get.json()["value"] == "default"


def test_create_node_history_action_with_uuid(client):
    # Create a node history action and specify the UUID it should use
    u = str(uuid.uuid4())
    create = client.post("/api/node/history/action/", json={"uuid": u, "value": "default"})
    assert create.status_code == status.HTTP_201_CREATED
    assert create.headers["Content-Location"]

    # Read it back using the UUID
    get = client.get(f"/api/node/history/action/{u}")
    assert get.status_code == status.HTTP_200_OK
    assert get.json()["uuid"] == u
    assert get.json()["description"] is None
    assert get.json()["value"] == "default"


def test_create_node_history_action_duplicate_value(client):
    # Create a node history action
    client.post("/api/node/history/action/", json={"value": "default"})

    # Ensure you cannot create another node history action with the same value
    create = client.post("/api/node/history/action/", json={"value": "default"})
    assert create.status_code == status.HTTP_409_CONFLICT


def test_create_node_history_action_invalid_uuid(client):
    create = client.post("/api/node/history/action/", json={"uuid": 1, "value": "default"})
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_node_history_action_invalid_value(client):
    create = client.post("/api/node/history/action/", json={"value": {"asdf": "asdf"}})
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_node_history_action_missing_value(client):
    create = client.post("/api/node/history/action/", json={})
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


#
# READ
#


def test_get_all_node_history_actions(client):
    # Create some node history actions
    client.post("/api/node/history/action/", json={"value": "default"})
    client.post("/api/node/history/action/", json={"value": "intel"})

    # Read them back
    get = client.get("/api/node/history/action/")
    assert get.status_code == status.HTTP_200_OK
    assert len(get.json()) == 2


def test_get_all_node_history_actions_empty(client):
    get = client.get("/api/node/history/action/")
    assert get.status_code == status.HTTP_200_OK
    assert get.json() == []


def test_get_invalid_node_history_action(client):
    get = client.get("/api/node/history/action/1")
    assert get.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_nonexistent_node_history_action(client):
    get = client.get(f"/api/node/history/action/{uuid.uuid4()}")
    assert get.status_code == status.HTTP_404_NOT_FOUND


#
# UPDATE
#


def test_update_node_history_action(client):
    # Create a node history action
    create = client.post("/api/node/history/action/", json={"value": "default"})

    # Update a single field
    update = client.put(create.headers["Content-Location"], json={"value": "test"})
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert update.headers["Content-Location"]

    # Read it back
    get = client.get(update.headers["Content-Location"])
    assert get.status_code == status.HTTP_200_OK
    assert get.json()["description"] is None
    assert get.json()["value"] == "test"


def test_update_node_history_action_multiple_fields(client):
    # Create a node history action
    create = client.post("/api/node/history/action/", json={"value": "default"})

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


def test_udpate_node_history_action_same_value(client):
    # Create a node history action
    create = client.post("/api/node/history/action/", json={"value": "default"})

    # Update a field to the same value
    update = client.put(create.headers["Content-Location"], json={"value": "default"})
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert update.headers["Content-Location"]

    # Read it back
    get = client.get(update.headers["Content-Location"])
    assert get.status_code == status.HTTP_200_OK
    assert get.json()["description"] is None
    assert get.json()["value"] == "default"


def test_update_node_history_action_duplicate_value(client):
    # Create some node history actions
    client.post("/api/node/history/action/", json={"value": "default"})
    create = client.post("/api/node/history/action/", json={"value": "intel"})

    # Ensure you cannot update a node history action value to one that already exists
    update = client.put(create.headers["Content-Location"], json={"value": "default"})
    assert update.status_code == status.HTTP_400_BAD_REQUEST


def test_update_node_history_action_invalid_uuid(client):
    update = client.put("/api/node/history/action/1", json={"value": "default"})
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_node_history_action_invalid_value(client):
    update = client.put(f"/api/node/history/action/{uuid.uuid4()}", json={"value": {"asdf": "asdf"}})
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_node_history_action_none_value(client):
    # Create a node history action
    create = client.post("/api/node/history/action/", json={"value": "default"})

    # Ensure you cannot update a node history action value to None
    update = client.put(create.headers["Content-Location"], json={"value": None})
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_nonexistent_node_history_action(client):
    update = client.put(f"/api/node/history/action/{uuid.uuid4()}", json={"value": "default"})
    assert update.status_code == status.HTTP_404_NOT_FOUND


#
# DELETE
#


def test_delete_node_history_action(client):
    # Create a node history action
    create = client.post("/api/node/history/action/", json={"value": "default"})

    # Delete it
    delete = client.delete(create.headers["Content-Location"])
    assert delete.status_code == status.HTTP_204_NO_CONTENT

    # Make sure it is gone
    get = client.get(create.headers["Content-Location"])
    assert get.status_code == status.HTTP_404_NOT_FOUND


def test_delete_invalid_node_history_action(client):
    delete = client.delete("/api/node/history/action/1")
    assert delete.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_delete_nonexistent_node_history_action(client):
    delete = client.delete(f"/api/node/history/action/{uuid.uuid4()}")
    assert delete.status_code == status.HTTP_404_NOT_FOUND
