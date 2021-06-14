import pytest
import uuid

from fastapi import status


#
# INVALID TESTS
#


@pytest.mark.parametrize(
    "key,value",
    [
        ("description", 123),
        ("description", ""),
        ("manual", 123),
        ("manual", None),
        ("manual", "True"),
        ("observable_types", 123),
        ("observable_types", None),
        ("observable_types", "test_type"),
        ("observable_types", [123]),
        ("observable_types", [None]),
        ("observable_types", [""]),
        ("observable_types", ["abc", 123]),
        ("uuid", 123),
        ("uuid", None),
        ("uuid", ""),
        ("uuid", "abc"),
    ],
)
def test_create_invalid_optional_fields(client, key, value):
    create = client.post("/api/analysis/module_type/", json={key: value, "value": "test"})
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.parametrize(
    "value",
    [
        (123),
        (None),
        (""),
    ],
)
def test_create_invalid_value(client, value):
    create = client.post("/api/analysis/module_type/", json={"value": value})
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_duplicate_value(client):
    # Create an analysis module type
    create = client.post("/api/analysis/module_type/", json={"value": "test"})
    assert create.status_code == status.HTTP_201_CREATED
    assert create.headers["Content-Location"]

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert get.status_code == status.HTTP_200_OK
    assert get.json()["description"] is None
    assert get.json()["manual"] is False
    assert get.json()["observable_types"] == []
    assert get.json()["value"] == "test"

    # Ensure you cannot create another analysis module type with the same value
    create = client.post("/api/analysis/module_type/", json={"value": "test"})
    assert create.status_code == status.HTTP_409_CONFLICT


def test_create_analysis_module_type_missing_value(client):
    create = client.post("/api/analysis/module_type/", json={"description": "test"})
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_analysis_module_type_nonexistent_type(client):
    create = client.post(
        "/api/analysis/module_type/",
        json={"value": "test", "observable_types": ["test_type"]},
    )
    assert create.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


@pytest.mark.parametrize(
    "value",
    [
        (None),
        ("Test"),
    ],
)
def test_create_valid_description(client, value):
    # Create the analysis module type
    create = client.post("/api/analysis/module_type/", json={"description": value, "value": "test"})
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert get.json()["description"] == value


@pytest.mark.parametrize(
    "value",
    [
        (True),
        (False),
    ],
)
def test_create_valid_manual(client, value):
    # Create the analysis module type
    create = client.post("/api/analysis/module_type/", json={"manual": value, "value": "test"})
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert get.json()["manual"] == value


@pytest.mark.parametrize(
    "value,list_length",
    [
        ([], 0),
        (["test_type"], 1),
        (["test_type1", "test_type2"], 2),
        (["test_type", "test_type"], 1),
    ],
)
def test_create_valid_observable_types(client, value, list_length):
    # Create the observable types. Need to only create unique values, otherwise the database will return a 409
    # conflict exception and will roll back the test's database session (causing the test to fail).
    for observable_type in list(set(value)):
        client.post("/api/observable/type/", json={"value": observable_type})

    # Create the analysis module type
    create = client.post("/api/analysis/module_type/", json={"observable_types": value, "value": "test"})
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert len(get.json()["observable_types"]) == list_length


def test_create_valid_uuid(client):
    uuid_ = str(uuid.uuid4())

    # Create the analysis module type
    create = client.post("/api/analysis/module_type/", json={"uuid": uuid_, "value": "test"})
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert get.json()["uuid"] == uuid_


def test_create_valid_value(client):
    # Create the analysis module type
    create = client.post("/api/analysis/module_type/", json={"value": "test"})
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert get.json()["value"] == "test"
