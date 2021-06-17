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
        ("uuid", ""),
        ("value", 123),
        ("value", None),
        ("value", ""),
    ],
)
def test_create_invalid_fields(client, key, value):
    create_json = {"value": "test"}
    create_json[key] = value
    create = client.post("/api/analysis/module_type/", json=create_json)
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.parametrize(
    "key",
    [
        ("value"),
    ],
)
def test_create_duplicate_unique_fields(client, key):
    # Create an object
    # Create an object
    create1_json = {"value": "test"}
    client.post("/api/analysis/module_type/", json=create1_json)

    # Ensure you cannot create another object with the same unique field value
    create2_json = {"value": "test2"}
    create2_json[key] = create1_json[key]
    create2 = client.post("/api/analysis/module_type/", json=create2_json)
    assert create2.status_code == status.HTTP_409_CONFLICT


@pytest.mark.parametrize(
    "key",
    [
        ("value"),
    ],
)
def test_create_missing_required_fields(client, key):
    create_json = {"value": "test"}
    del create_json[key]
    create = client.post("/api/analysis/module_type/", json=create_json)
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_nonexistent_type(client):
    create = client.post(
        "/api/analysis/module_type/",
        json={"value": "test", "observable_types": ["test_type"]},
    )
    assert create.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


@pytest.mark.parametrize(
    "key,value",
    [
        ("description", None),
        ("description", "test"),
        ("manual", True),
        ("manual", False),
        ("uuid", str(uuid.uuid4()))
    ],
)
def test_create_valid_optional_fields(client, key, value):
    # Create the object
    create = client.post("/api/analysis/module_type/", json={key: value, "value": "test"})
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert get.json()[key] == value


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


def test_create_valid_required_fields(client):
    # Create the object
    create = client.post("/api/analysis/module_type/", json={"value": "test"})
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert get.json()["value"] == "test"
