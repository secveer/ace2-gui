import uuid

from fastapi import status


"""
NOTE: There are no tests for the foreign key constraints, namely deleting a Disposition that is tied to and Alert.
The DELETE endpoint will need to be updated once the Alert endpoints are in place in order to account for this.
"""


#
# CREATE
#


def test_create_disposition(client):
    # Create a disposition
    create = client.post("/api/alert/disposition/", json={"rank": 1, "value": "FALSE_POSITIVE"})
    assert create.status_code == status.HTTP_201_CREATED
    assert create.headers["Content-Location"]

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert get.status_code == status.HTTP_200_OK
    assert get.json()["description"] is None
    assert get.json()["rank"] == 1
    assert get.json()["value"] == "FALSE_POSITIVE"


def test_create_disposition_with_uuid(client):
    # Create a disposition and specify the UUID it should use
    u = str(uuid.uuid4())
    create = client.post(
        "/api/alert/disposition/",
        json={"uuid": u, "rank": 1, "value": "FALSE_POSITIVE"},
    )
    assert create.status_code == status.HTTP_201_CREATED
    assert create.headers["Content-Location"]

    # Read it back using the UUID
    get = client.get(f"/api/alert/disposition/{u}")
    assert get.status_code == status.HTTP_200_OK
    assert get.json()["uuid"] == u
    assert get.json()["description"] is None
    assert get.json()["rank"] == 1
    assert get.json()["value"] == "FALSE_POSITIVE"


def test_create_disposition_duplicate_rank(client):
    # Create a disposition
    client.post("/api/alert/disposition/", json={"rank": 1, "value": "FALSE_POSITIVE"})

    # Ensure you cannot create another disposition with the same rank
    create = client.post("/api/alert/disposition/", json={"rank": 1, "value": "IGNORE"})
    assert create.status_code == status.HTTP_409_CONFLICT


def test_create_disposition_duplicate_value(client):
    # Create a disposition
    client.post("/api/alert/disposition/", json={"rank": 1, "value": "FALSE_POSITIVE"})

    # Ensure you cannot create another disposition with the same value
    create = client.post("/api/alert/disposition/", json={"rank": 2, "value": "FALSE_POSITIVE"})
    assert create.status_code == status.HTTP_409_CONFLICT


def test_create_disposition_invalid_rank(client):
    create = client.post("/api/alert/disposition/", json={"rank": "asdf", "value": "FALSE_POSITIVE"})
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_disposition_invalid_uuid(client):
    create = client.post(
        "/api/alert/disposition/",
        json={"uuid": 1, "rank": 1, "value": "FALSE_POSITIVE"},
    )
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_disposition_invalid_value(client):
    create = client.post("/api/alert/disposition/", json={"rank": 1, "value": {"asdf": "asdf"}})
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_disposition_missing_rank(client):
    create = client.post("/api/alert/disposition/", json={"value": "FALSE_POSITIVE"})
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_disposition_missing_value(client):
    create = client.post("/api/alert/disposition/", json={"rank": 1})
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


#
# READ
#


def test_get_all_dispositions(client):
    # Create some dispositions
    client.post("/api/alert/disposition/", json={"rank": 1, "value": "FALSE_POSITIVE"})
    client.post("/api/alert/disposition/", json={"rank": 2, "value": "IGNORE"})

    # Read them back
    get = client.get("/api/alert/disposition/")
    assert get.status_code == status.HTTP_200_OK
    assert len(get.json()) == 2


def test_get_all_dispositions_empty(client):
    get = client.get("/api/alert/disposition/")
    assert get.status_code == status.HTTP_200_OK
    assert get.json() == []


def test_get_invalid_disposition(client):
    get = client.get("/api/alert/disposition/1")
    assert get.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_nonexistent_disposition(client):
    get = client.get(f"/api/alert/disposition/{uuid.uuid4()}")
    assert get.status_code == status.HTTP_404_NOT_FOUND


#
# UPDATE
#


def test_update_disposition(client):
    # Create a disposition
    create = client.post("/api/alert/disposition/", json={"rank": 1, "value": "FALSE_POSITIVE"})

    # Update a single field
    update = client.put(create.headers["Content-Location"], json={"rank": 2})
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert update.headers["Content-Location"]

    # Read it back
    get = client.get(update.headers["Content-Location"])
    assert get.status_code == status.HTTP_200_OK
    assert get.json()["description"] is None
    assert get.json()["rank"] == 2
    assert get.json()["value"] == "FALSE_POSITIVE"


def test_update_disposition_multiple_fields(client):
    # Create a disposition
    create = client.post("/api/alert/disposition/", json={"rank": 1, "value": "FALSE_POSITIVE"})

    # Update multiple fields
    update = client.put(
        create.headers["Content-Location"],
        json={"description": "Test", "rank": 2, "value": "UPDATED"},
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert update.headers["Content-Location"]

    # Read it back
    get = client.get(update.headers["Content-Location"])
    assert get.status_code == status.HTTP_200_OK
    assert get.json()["description"] == "Test"
    assert get.json()["rank"] == 2
    assert get.json()["value"] == "UPDATED"


def test_udpate_disposition_same_value(client):
    # Create a disposition
    create = client.post("/api/alert/disposition/", json={"rank": 1, "value": "FALSE_POSITIVE"})

    # Update a field to the same value
    update = client.put(create.headers["Content-Location"], json={"rank": 1})
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert update.headers["Content-Location"]

    # Read it back
    get = client.get(update.headers["Content-Location"])
    assert get.status_code == status.HTTP_200_OK
    assert get.json()["description"] is None
    assert get.json()["rank"] == 1
    assert get.json()["value"] == "FALSE_POSITIVE"


def test_update_disposition_duplicate_rank(client):
    # Create some dispositions
    client.post("/api/alert/disposition/", json={"rank": 1, "value": "FALSE_POSITIVE"})
    create = client.post("/api/alert/disposition/", json={"rank": 2, "value": "IGNORE"})

    # Ensure you cannot update a disposition rank to one that already exists
    update = client.put(create.headers["Content-Location"], json={"rank": 1})
    assert update.status_code == status.HTTP_400_BAD_REQUEST


def test_update_disposition_duplicate_value(client):
    # Create some dispositions
    client.post("/api/alert/disposition/", json={"rank": 1, "value": "FALSE_POSITIVE"})
    create = client.post("/api/alert/disposition/", json={"rank": 2, "value": "IGNORE"})

    # Ensure you cannot update a disposition rank to one that already exists
    update = client.put(create.headers["Content-Location"], json={"value": "FALSE_POSITIVE"})
    assert update.status_code == status.HTTP_400_BAD_REQUEST


def test_update_disposition_invalid_rank(client):
    update = client.put(f"/api/alert/disposition/{uuid.uuid4()}", json={"rank": "asdf"})
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_disposition_invalid_uuid(client):
    update = client.put("/api/alert/disposition/1", json={"rank": 1})
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_disposition_invalid_value(client):
    update = client.put(f"/api/alert/disposition/{uuid.uuid4()}", json={"value": {"asdf": "asdf"}})
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_disposition_none_rank(client):
    # Create a disposition
    create = client.post("/api/alert/disposition/", json={"rank": 1, "value": "FALSE_POSITIVE"})

    # Ensure you cannot update a disposition rank to None
    update = client.put(create.headers["Content-Location"], json={"rank": None})
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_disposition_none_value(client):
    # Create a disposition
    create = client.post("/api/alert/disposition/", json={"rank": 1, "value": "FALSE_POSITIVE"})

    # Ensure you cannot update a disposition value to None
    update = client.put(create.headers["Content-Location"], json={"value": None})
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_nonexistent_disposition(client):
    update = client.put(f"/api/alert/disposition/{uuid.uuid4()}", json={"value": "FALSE_POSITIVE"})
    assert update.status_code == status.HTTP_404_NOT_FOUND


#
# DELETE
#


def test_delete_disposition(client):
    # Create a disposition
    create = client.post("/api/alert/disposition/", json={"rank": 1, "value": "FALSE_POSITIVE"})

    # Delete it
    delete = client.delete(create.headers["Content-Location"])
    assert delete.status_code == status.HTTP_204_NO_CONTENT

    # Make sure it is gone
    get = client.get(create.headers["Content-Location"])
    assert get.status_code == status.HTTP_404_NOT_FOUND


def test_delete_invalid_disposition(client):
    delete = client.delete("/api/alert/disposition/1")
    assert delete.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_delete_nonexistent_disposition(client):
    delete = client.delete(f"/api/alert/disposition/{uuid.uuid4()}")
    assert delete.status_code == status.HTTP_404_NOT_FOUND
