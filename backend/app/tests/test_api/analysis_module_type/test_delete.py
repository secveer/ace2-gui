import uuid

from fastapi import status


"""
NOTE: There are no tests for the foreign key constraints, namely deleting an AnalysisModuleType that is tied to an
Analysis. The DELETE endpoint will need to be updated once the Analysis endpoints are in place in order to account
for this.
"""


#
# INVALID TESTS
#


def test_delete_invalid_analysis_module_type(client):
    delete = client.delete("/api/observable/type/1")
    assert delete.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_delete_nonexistent_analysis_module_type(client):
    delete = client.delete(f"/api/observable/type/{uuid.uuid4()}")
    assert delete.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


def test_delete_analysis_module_type(client):
    # Create an observable type
    type_create = client.post("/api/observable/type/", json={"value": "test_type"})

    # Create the analysis module type
    create = client.post(
        f"/api/analysis/module_type/",
        json={"observable_types": ["test_type"], "value": "initial"},
    )
    assert create.status_code == status.HTTP_201_CREATED

    # Delete it
    delete = client.delete(create.headers["Content-Location"])
    assert delete.status_code == status.HTTP_204_NO_CONTENT

    # Make sure it is gone
    get = client.get(create.headers["Content-Location"])
    assert get.status_code == status.HTTP_404_NOT_FOUND

    # Make sure the observable type is still there
    get = client.get(type_create.headers["Content-Location"])
    assert get.status_code == status.HTTP_200_OK
    assert get.json()["value"] == "test_type"
