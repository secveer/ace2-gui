import json
import pytest
import uuid

from fastapi import status

from tests.api.node import (
    INVALID_UPDATE_FIELDS,
    NONEXISTENT_FIELDS,
    VALID_DIRECTIVES,
    VALID_TAGS,
    VALID_THREAT_ACTOR,
    VALID_THREATS,
)


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
        ("error_message", 123),
        ("error_message", ""),
        ("stack_trace", 123),
        ("stack_trace", ""),
        ("summary", 123),
        ("summary", ""),
    ],
)
def test_update_invalid_fields(client, key, value):
    update = client.put(f"/api/analysis/{uuid.uuid4()}", json={key: value, "version": str(uuid.uuid4())})
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert key in update.text


@pytest.mark.parametrize(
    "key,value",
    INVALID_UPDATE_FIELDS,
)
def test_update_invalid_node_fields(client, key, value):
    update = client.put(f"/api/analysis/{uuid.uuid4()}", json={"version": str(uuid.uuid4()), key: value})
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert key in update.text


def test_update_invalid_uuid(client):
    update = client.put("/api/analysis/1", json={"version": str(uuid.uuid4())})
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_nonexistent_analysis_module_type(client):
    # Create an analysis
    version = str(uuid.uuid4())
    create = client.post("/api/analysis/", json={"version": version})

    # Make sure you cannot update it to use a nonexistent analysis module type
    update = client.put(
        create.headers["Content-Location"],
        json={"analysis_module_type": str(uuid.uuid4()), "version": version}
    )
    assert update.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize(
    "key,value",
    NONEXISTENT_FIELDS,
)
def test_update_nonexistent_node_fields(client, key, value):
    # Create an analysis
    version = str(uuid.uuid4())
    create = client.post("/api/analysis/", json={"version": version})

    # Make sure you cannot update it to use a nonexistent node field value
    update = client.put(
        create.headers["Content-Location"],
        json={key: value, "version": version}
    )
    assert update.status_code == status.HTTP_404_NOT_FOUND


def test_update_nonexistent_uuid(client):
    update = client.put(f"/api/analysis/{uuid.uuid4()}", json={"version": str(uuid.uuid4())})
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
    version = str(uuid.uuid4())
    create = client.post(
        "/api/analysis/",
        json={"analysis_module_type": analysis_module_type_uuid1, "version": version}
    )
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert get.json()["analysis_module_type"]["uuid"] == analysis_module_type_uuid1

    # Update the analysis module type
    update = client.put(
        create.headers["Content-Location"],
        json={"analysis_module_type": analysis_module_type_uuid2, "version": version}
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert get.json()["analysis_module_type"]["uuid"] == analysis_module_type_uuid2
    assert get.json()["version"] != version


@pytest.mark.parametrize(
    "values",
    VALID_DIRECTIVES,
)
def test_update_valid_node_directives(client, values):
    # Create a node
    version = str(uuid.uuid4())
    create = client.post("/api/analysis/", json={"version": version})
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert get.json()["directives"] == []

    # Create the directives. Need to only create unique values, otherwise the database will return a 409
    # conflict exception and will roll back the test's database session (causing the test to fail).
    for value in list(set(values)):
        client.post("/api/node/directive/", json={"value": value})

    # Update the node
    update = client.put(
        create.headers["Content-Location"],
        json={"directives": values, "version": version}
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert len(get.json()["directives"]) == len(list(set(values)))
    assert get.json()["version"] != version


@pytest.mark.parametrize(
    "values",
    VALID_TAGS,
)
def test_update_valid_node_tags(client, values):
    # Create a node
    version = str(uuid.uuid4())
    create = client.post("/api/analysis/", json={"version": version})
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert get.json()["tags"] == []

    # Create the tags. Need to only create unique values, otherwise the database will return a 409
    # conflict exception and will roll back the test's database session (causing the test to fail).
    for value in list(set(values)):
        client.post("/api/node/tag/", json={"value": value})

    # Update the node
    update = client.put(
        create.headers["Content-Location"],
        json={"tags": values, "version": version}
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert len(get.json()["tags"]) == len(list(set(values)))
    assert get.json()["version"] != version


@pytest.mark.parametrize(
    "value",
    VALID_THREAT_ACTOR,
)
def test_update_valid_node_threat_actor(client, value):
    # Create a node
    version = str(uuid.uuid4())
    create = client.post("/api/analysis/", json={"version": version})
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert get.json()["threat_actor"] is None

    # Create the threat actor
    if value:
        client.post("/api/node/threat_actor/", json={"value": value})

    # Update the node
    update = client.put(
        create.headers["Content-Location"],
        json={"threat_actor": value, "version": version}
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT

    # Read it back
    get = client.get(create.headers["Content-Location"])
    if value:
        assert get.json()["threat_actor"]["value"] == value
    else:
        assert get.json()["threat_actor"] is None

    assert get.json()["version"] != version


@pytest.mark.parametrize(
    "values",
    VALID_THREATS,
)
def test_update_valid_node_threats(client, values):
    # Create a node
    version = str(uuid.uuid4())
    create = client.post("/api/analysis/", json={"version": version})
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert get.json()["directives"] == []

    # Create a threat type
    client.post("/api/node/threat/type/", json={"value": "test_type"})

    # Create the threats. Need to only create unique values, otherwise the database will return a 409
    # conflict exception and will roll back the test's database session (causing the test to fail).
    for value in list(set(values)):
        client.post("/api/node/threat/", json={"types": ["test_type"], "value": value})

    # Update the node
    update = client.put(
        create.headers["Content-Location"],
        json={"threats": values, "version": version}
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert len(get.json()["threats"]) == len(list(set(values)))
    assert get.json()["version"] != version


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
    version = str(uuid.uuid4())
    create_json = {"version": version}
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
    update = client.put(create.headers["Content-Location"], json={"version": version, key: updated_value})
    assert update.status_code == status.HTTP_204_NO_CONTENT

    # Read it back
    get = client.get(create.headers["Content-Location"])

    # If the test is for details, make sure the JSON form of the supplied string matches
    if key == "details":
        assert get.json()[key] == json.loads(updated_value)
    else:
        assert get.json()[key] == updated_value

    assert get.json()["version"] != version
