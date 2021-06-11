import uuid

from fastapi import status


#
# INVALID TESTS
#


def test_get_invalid_analysis_module_type(client):
    get = client.get("/api/analysis/module_type/1")
    assert get.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_nonexistent_analysis_module_type(client):
    get = client.get(f"/api/analysis/module_type/{uuid.uuid4()}")
    assert get.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


def test_get_all_analysis_module_types(client):
    # Create some analysis module types
    client.post("/api/analysis/module_type/", json={"value": "test"})
    client.post("/api/analysis/module_type/", json={"value": "test2"})

    # Read them back
    get = client.get("/api/analysis/module_type/")
    assert get.status_code == status.HTTP_200_OK
    assert len(get.json()) == 2


def test_get_all_analysis_module_types_empty(client):
    get = client.get("/api/analysis/module_type/")
    assert get.status_code == status.HTTP_200_OK
    assert get.json() == []
