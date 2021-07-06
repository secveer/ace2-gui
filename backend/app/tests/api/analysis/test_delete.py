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
    delete = client.delete("/api/analysis/1")
    assert delete.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_delete_nonexistent_uuid(client):
    delete = client.delete(f"/api/analysis/{uuid.uuid4()}")
    assert delete.status_code == status.HTTP_404_NOT_FOUND


def test_delete_non_manual(client):
    # Create the non-manual analysis
    create = client.post("/api/analysis/", json={"manual": False})

    # You should not be able to delete it
    delete = client.delete(create.headers["Content-Location"])
    assert delete.status_code == status.HTTP_403_FORBIDDEN


#
# VALID TESTS
#


def test_delete(client):
    # Create an analysis module type
    analysis_module_type_uuid = str(uuid.uuid4())
    analysis_module_type_create = client.post(
        "/api/analysis/module_type/",
        json={"uuid": analysis_module_type_uuid, "value": "test", "version": "1.0.0"}
    )

    # TODO: Create an observable instance when those endpoints are finished

    # Create the analysis. You can only delete manual=True analyses.
    create = client.post("/api/analysis/", json={"analysis_module_type": analysis_module_type_uuid, "manual": True})
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

    # Make sure the analysis module type is still there
    get = client.get(analysis_module_type_create.headers["Content-Location"])
    assert get.status_code == status.HTTP_200_OK
    assert get.json()["value"] == "test"

    # TODO: Deleting an analysis should probably also delete the observable instances in it.
