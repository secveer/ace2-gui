import uuid

from fastapi import status


#
# INVALID TESTS
#


def test_get_invalid_uuid(client):
    get = client.get("/api/observable/1")
    assert get.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_nonexistent_uuid(client):
    get = client.get(f"/api/observable/{uuid.uuid4()}")
    assert get.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


def test_get_all(client):
    # Create an observable type
    client.post("/api/observable/type/", json={"value": "test_type"})

    # Create some objects
    client.post("/api/observable/", json={"type": "test_type", "value": "test"})
    client.post("/api/observable/", json={"type": "test_type", "value": "test2"})

    # Read them back
    get = client.get("/api/observable/")
    assert get.status_code == status.HTTP_200_OK
    assert len(get.json()) == 2


def test_get_all_empty(client):
    get = client.get("/api/observable/")
    assert get.status_code == status.HTTP_200_OK
    assert get.json() == []
