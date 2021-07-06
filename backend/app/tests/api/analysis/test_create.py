import json
import pytest
import uuid

from fastapi import status


#
# INVALID TESTS
#


@pytest.mark.parametrize(
    "key,value",
    [
        ("analysis_module_type", 123),
        ("analysis_module_type", ""),
        ("analysis_module_type", "abc"),
        ("details", 123),
        ("details", ""),
        ("details", "abc"),
        ("details", []),
        ("discovered_observables", 123),
        ("discovered_observables", ""),
        ("discovered_observables", "abc"),
        ("discovered_observables", [123]),
        ("discovered_observables", [None]),
        ("discovered_observables", [""]),
        ("discovered_observables", ["abc", 123]),
        ("error_message", 123),
        ("error_message", ""),
        ("manual", 123),
        ("manual", None),
        ("manual", "True"),
        ("stack_trace", 123),
        ("stack_trace", ""),
        ("summary", 123),
        ("summary", ""),
        ("uuid", 123),
        ("uuid", None),
        ("uuid", ""),
        ("uuid", "abc"),
    ],
)
def test_create_invalid_fields(client, key, value):
    create_json = {"value": "test"}
    create_json[key] = value
    create = client.post("/api/analysis/", json=create_json)
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.parametrize(
    "key",
    [
        ("uuid"),
    ],
)
def test_create_duplicate_unique_fields(client, key):
    # Create an object
    create1_json = {"uuid": str(uuid.uuid4())}
    client.post("/api/analysis/", json=create1_json)

    # Ensure you cannot create another object with the same unique field value
    create2_json = {}
    create2_json[key] = create1_json[key]
    create2 = client.post("/api/analysis/", json=create2_json)
    assert create2.status_code == status.HTTP_409_CONFLICT


def test_create_nonexistent_analysis_module_type(client):
    create = client.post("/api/analysis/", json={"analysis_module_type": str(uuid.uuid4())})
    assert create.status_code == status.HTTP_404_NOT_FOUND


def test_create_nonexistent_discovered_observables(client):
    create = client.post("/api/analysis/", json={"discovered_observables": [str(uuid.uuid4())]})
    assert create.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


@pytest.mark.parametrize(
    "key,value",
    [
        ("details", None),
        ("details", "{}"),
        ("details", '{"foo": "bar"}'),
        ("error_message", None),
        ("error_message", "test"),
        ("manual", True),
        ("manual", False),
        ("stack_trace", None),
        ("stack_trace", "test"),
        ("summary", None),
        ("summary", "test"),
        ("uuid", str(uuid.uuid4()))
    ],
)
def test_create_valid_optional_fields(client, key, value):
    # Create the object
    create = client.post("/api/analysis/", json={key: value})
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client.get(create.headers["Content-Location"])

    # If the test is for details, make sure the JSON form of the supplied string matches
    if key == "details" and value:
        assert get.json()[key] == json.loads(value)
    else:
        assert get.json()[key] == value


def test_create_valid_analysis_module_type(client):
    # Create an analysis module type
    analysis_module_type_uuid = str(uuid.uuid4())
    client.post(
        "/api/analysis/module_type/",
        json={"uuid": analysis_module_type_uuid, "value": "test", "version": "1.0.0"}
    )

    # Use the analysis module type to create a new analysis
    create = client.post("/api/analysis/", json={"analysis_module_type": analysis_module_type_uuid})
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert get.json()["analysis_module_type"]["uuid"] == analysis_module_type_uuid


# TODO: Fill out this test when observable instance endpoints are finished
def test_create_valid_discovered_observables(client):
    pass


def test_create_valid_required_fields(client):
    # Create the object
    create = client.post("/api/analysis/", json={})
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back, but since there are no required fields to create the analysis, there is nothing to verify.
    get = client.get(create.headers["Content-Location"])
    assert get.status_code == 200
