import uuid

from fastapi import status


#
# INVALID TESTS
#


def test_get_invalid_uuid(client):
    get = client.get("/api/user/1")
    assert get.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_nonexistent_uuid(client):
    get = client.get(f"/api/user/{uuid.uuid4()}")
    assert get.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


def test_get_all(client):
    # Create an alert queue
    client.post("/api/alert/queue/", json={"value": "test_queue"})

    # Create a user role
    client.post("/api/user/role/", json={"value": "test_role"})

    # Create some objects
    create1_json = {
        "default_alert_queue": "test_queue",
        "display_name": "John Doe",
        "email": "john@test.com",
        "password": "abcd1234",
        "roles": ["test_role"],
        "username": "johndoe",
    }
    client.post("/api/user/", json=create1_json)

    create2_json = {
        "default_alert_queue": "test_queue",
        "display_name": "Jane Doe",
        "email": "jane@test.com",
        "password": "wxyz6789",
        "roles": ["test_role"],
        "username": "janedoe",
    }
    client.post("/api/user/", json=create2_json)

    # Read them back
    get = client.get("/api/user/")
    assert get.status_code == status.HTTP_200_OK
    assert len(get.json()) == 2


def test_get_all_empty(client):
    get = client.get("/api/user/")
    assert get.status_code == status.HTTP_200_OK
    assert get.json() == []
