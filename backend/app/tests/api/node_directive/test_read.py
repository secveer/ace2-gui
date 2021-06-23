import uuid

from fastapi import status


#
# INVALID TESTS
#


def test_get_invalid_uuid(client):
    get = client.get("/api/node/directive/1")
    assert get.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_nonexistent_uuid(client):
    get = client.get(f"/api/node/directive/{uuid.uuid4()}")
    assert get.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


def test_get_all(client):
    # Create some objects
    client.post("/api/node/directive/", json={"value": "test"})
    client.post("/api/node/directive/", json={"value": "test2"})

    # Read them back
    get = client.get("/api/node/directive/")
    assert get.status_code == status.HTTP_200_OK
    assert len(get.json()) == 2


def test_get_all_empty(client):
    get = client.get("/api/node/directive/")
    assert get.status_code == status.HTTP_200_OK
    assert get.json() == []
