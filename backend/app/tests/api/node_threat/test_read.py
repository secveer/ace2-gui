import uuid

from fastapi import status


#
# INVALID TESTS
#


def test_get_invalid_uuid(client):
    get = client.get("/api/node/threat/1")
    assert get.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_nonexistent_uuid(client):
    get = client.get(f"/api/node/threat/{uuid.uuid4()}")
    assert get.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


def test_get_all(client):
    # Create a node threat type
    client.post("/api/node/threat/type/", json={"value": "test_type"})

    # Create some objects
    client.post("/api/node/threat/", json={"types": ["test_type"], "value": "test"})
    client.post("/api/node/threat/", json={"types": ["test_type"], "value": "test2"})

    # Read them back
    get = client.get("/api/node/threat/")
    assert get.status_code == status.HTTP_200_OK
    assert len(get.json()) == 2


def test_get_all_empty(client):
    get = client.get("/api/node/threat/")
    assert get.status_code == status.HTTP_200_OK
    assert get.json() == []
