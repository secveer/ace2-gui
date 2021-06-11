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
        ("value", 123),
        ("value", None),
        ("value", ""),
    ],
)
def test_update_invalid_fields(client, key, value):
    update = client.put(
        f"/api/analysis/module_type/{uuid.uuid4()}", json={key: value}
    )
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_invalid_uuid(client):
    update = client.put(f"/api/analysis/module_type/1", json={"value": "test_type"})
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_duplicate_value(client):
    # Create some analysis module types
    client.post("/api/analysis/module_type/", json={"value": "default"})
    create = client.post("/api/analysis/module_type/", json={"value": "test_type"})

    # Ensure you cannot update an analysis module type value to one that already exists
    update = client.put(create.headers["Content-Location"], json={"value": "default"})
    assert update.status_code == status.HTTP_400_BAD_REQUEST


def test_update_nonexistent_uuid(client):
    update = client.put(
        f"/api/analysis/module_type/{uuid.uuid4()}", json={"value": "test"}
    )
    assert update.status_code == status.HTTP_404_NOT_FOUND


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
def test_update_valid_description(client, value):
    # Create the analysis module type
    create = client.post(
        f"/api/analysis/module_type/", json={"description": "initial", "value": "test"}
    )
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert get.json()["description"] == "initial"

    # Update it
    update = client.put(create.headers["Content-Location"], json={"description": value})
    assert update.status_code == status.HTTP_204_NO_CONTENT

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
def test_update_valid_manual(client, value):
    # Create the analysis module type
    create = client.post(
        f"/api/analysis/module_type/", json={"manual": not value, "value": "test"}
    )
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert get.json()["manual"] is not value

    # Update it
    update = client.put(create.headers["Content-Location"], json={"manual": value})
    assert update.status_code == status.HTTP_204_NO_CONTENT

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert get.json()["manual"] is value


@pytest.mark.parametrize(
    "value",
    [
        ([]),
        (["new_type"]),
        (["new_type1", "new_type2"]),
    ],
)
def test_update_valid_observable_types(client, value):
    # Create some observable types
    initial_observable_types = ["test_type1", "test_type2", "test_type3"]
    for observable_type in initial_observable_types:
        client.post("/api/observable/type/", json={"value": observable_type})

    # Create the analysis module type
    create = client.post(
        f"/api/analysis/module_type/",
        json={"observable_types": initial_observable_types, "value": "test"},
    )
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert len(get.json()["observable_types"]) == len(initial_observable_types)

    # Create the new observable types
    for observable_type in value:
        client.post("/api/observable/type/", json={"value": observable_type})

    # Update it
    update = client.put(
        create.headers["Content-Location"], json={"observable_types": value}
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert len(get.json()["observable_types"]) == len(value)


@pytest.mark.parametrize(
    "value",
    [
        ("initial"),
        ("new_value"),
    ],
)
def test_update_valid_value(client, value):
    # Create the analysis module type
    create = client.post(f"/api/analysis/module_type/", json={"value": "initial"})
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert get.json()["value"] == "initial"

    # Update it
    update = client.put(create.headers["Content-Location"], json={"value": value})
    assert update.status_code == status.HTTP_204_NO_CONTENT

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert get.json()["value"] == value
