import uuid

from fastapi import status


"""
NOTE: There are no tests for the foreign key constraints. The DELETE endpoint will need to be updated once the endpoints
are in place in order to account for this.
"""


#
# INVALID TESTS
#


def test_delete_invalid_uuid(client):
    delete = client.delete("/api/node/threat/1")
    assert delete.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_delete_nonexistent_uuid(client):
    delete = client.delete(f"/api/node/threat/{uuid.uuid4()}")
    assert delete.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


def test_delete(client):
    # Create a node threat type
    type_create = client.post("/api/node/threat/type/", json={"value": "test_type"})

    # Create the object
    create = client.post("/api/node/threat/", json={"types": ["test_type"], "value": "test"})
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert get.status_code == status.HTTP_200_OK

    # Delete it
    delete = client.delete(create.headers["Content-Location"])
    assert delete.status_code == status.HTTP_204_NO_CONTENT

    # Make sure it is gone
    get = client.get(create.headers["Content-Location"])
    assert get.status_code == status.HTTP_404_NOT_FOUND

    # Make sure the node threat type is still there
    get = client.get(type_create.headers["Content-Location"])
    assert get.status_code == status.HTTP_200_OK
    assert get.json()["value"] == "test_type"
