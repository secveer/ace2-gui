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
    ],
)
def test_update_invalid_fields(client, key, value):
    update = client.put(f"/api/analysis/{uuid.uuid4()}", json={key: value})
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_invalid_uuid(client):
    update = client.put("/api/analysis/1", json={})
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_nonexistent_analysis_module_type(client):
    # Create an analysis
    create = client.post("/api/analysis/", json={})

    # Make sure you cannot update it to use a nonexistent analysis module type
    update = client.put(create.headers["Content-Location"], json={"analysis_module_type": str(uuid.uuid4())})
    assert update.status_code == status.HTTP_404_NOT_FOUND


def test_update_nonexistent_discovered_observables(client):
    # Create an analysis
    create = client.post("/api/analysis/", json={})

    # Make sure you cannot update it to use a nonexistent discovered observable
    update = client.put(create.headers["Content-Location"], json={"discovered_observables": [str(uuid.uuid4())]})
    assert update.status_code == status.HTTP_404_NOT_FOUND


def test_update_nonexistent_uuid(client):
    update = client.put(f"/api/analysis/{uuid.uuid4()}", json={})
    assert update.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


def test_update_analysis_module_type(client):
    # Create some analysis module types
    analysis_module_type_uuid1 = str(uuid.uuid4())
    client.post(
        "/api/analysis/module_type/",
        json={"uuid": analysis_module_type_uuid1, "value": "test", "version": "1.0.0"}
    )

    analysis_module_type_uuid2 = str(uuid.uuid4())
    client.post(
        "/api/analysis/module_type/",
        json={"uuid": analysis_module_type_uuid2, "value": "test2", "version": "1.0.0"}
    )

    # Use the analysis module type to create a new analysis
    create = client.post("/api/analysis/", json={"analysis_module_type": analysis_module_type_uuid1})
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert get.json()["analysis_module_type"]["uuid"] == analysis_module_type_uuid1

    # Update the analysis module type
    update = client.put(create.headers["Content-Location"], json={"analysis_module_type": analysis_module_type_uuid2})
    assert update.status_code == status.HTTP_204_NO_CONTENT

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert get.json()["analysis_module_type"]["uuid"] == analysis_module_type_uuid2


def test_update_detected_observables(client):
    # TODO: Write this test when the observable instance endpoints are finished
    pass


@pytest.mark.parametrize(
    "key,initial_value,updated_value",
    [
        ("details", None, '{"foo": "bar"}'),
        ("details", '{"foo": "bar"}', '{"foo": "bar"}'),
        ("error_message", None, "test"),
        ("error_message", "test", "test"),
        ("stack_trace", None, "test"),
        ("stack_trace", "test", "test"),
        ("summary", None, "test"),
        ("summary", "test", "test"),
    ],
)
def test_update(client, key, initial_value, updated_value):
    # Create the object
    create_json = {}
    create_json[key] = initial_value
    create = client.post("/api/analysis/", json=create_json)
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client.get(create.headers["Content-Location"])

    # If the test is for details, make sure the JSON form of the supplied string matches
    if key == "details" and initial_value:
        assert get.json()[key] == json.loads(initial_value)
    else:
        assert get.json()[key] == initial_value

    # Update it
    update = client.put(create.headers["Content-Location"], json={key: updated_value})
    assert update.status_code == status.HTTP_204_NO_CONTENT

    # Read it back
    get = client.get(create.headers["Content-Location"])

    # If the test is for details, make sure the JSON form of the supplied string matches
    if key == "details":
        assert get.json()[key] == json.loads(updated_value)
    else:
        assert get.json()[key] == updated_value
