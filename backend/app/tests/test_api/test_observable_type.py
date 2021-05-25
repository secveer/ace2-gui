import uuid


"""
NOTE: There are no tests for the foreign key constraints, namely deleting an ObservableType that is tied to an Observable.
The DELETE endpoint will need to be updated once the Observable endpoints are in place in order to account for this.
"""


#
# CREATE
#


def test_create_observable_type(client):
    # Create an observable type
    create = client.post("/api/observable/type/", json={"value": "default"})
    assert create.status_code == 201
    assert create.headers["Content-Location"]

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert get.status_code == 200
    assert get.json()["description"] is None
    assert get.json()["value"] == "default"


def test_create_observable_type_with_uuid(client):
    # Create an observable type and specify the UUID it should use
    u = str(uuid.uuid4())
    create = client.post("/api/observable/type/", json={"uuid": u, "value": "default"})
    assert create.status_code == 201
    assert create.headers["Content-Location"]

    # Read it back using the UUID
    get = client.get(f"/api/observable/type/{u}")
    assert get.status_code == 200
    assert get.json()["uuid"] == u
    assert get.json()["description"] is None
    assert get.json()["value"] == "default"


def test_create_observable_type_duplicate_value(client):
    # Create an observable type
    client.post("/api/observable/type/", json={"value": "default"})

    # Ensure you cannot create another observable type with the same value
    create = client.post("/api/observable/type/", json={"value": "default"})
    assert create.status_code == 409


def test_create_observable_type_invalid_uuid(client):
    create = client.post("/api/observable/type/", json={"uuid": 1, "value": "default"})
    assert create.status_code == 422


def test_create_observable_type_invalid_value(client):
    create = client.post("/api/observable/type/", json={"value": {"asdf": "asdf"}})
    assert create.status_code == 422


def test_create_observable_type_missing_value(client):
    create = client.post("/api/observable/type/", json={})
    assert create.status_code == 422


#
# READ
#


def test_get_all_observable_types(client):
    # Create some observable types
    client.post("/api/observable/type/", json={"value": "default"})
    client.post("/api/observable/type/", json={"value": "intel"})

    # Read them back
    get = client.get("/api/observable/type/")
    assert get.status_code == 200
    assert len(get.json()) == 2


def test_get_all_observable_types_empty(client):
    get = client.get("/api/observable/type/")
    assert get.status_code == 200
    assert get.json() == []


def test_get_invalid_observable_type(client):
    get = client.get("/api/observable/type/1")
    assert get.status_code == 422


def test_get_nonexistent_observable_type(client):
    get = client.get(f"/api/observable/type/{uuid.uuid4()}")
    assert get.status_code == 404


#
# UPDATE
#


def test_update_observable_type(client):
    # Create an observable type
    create = client.post("/api/observable/type/", json={"value": "default"})

    # Update a single field
    update = client.put(create.headers["Content-Location"], json={"value": "test"})
    assert update.status_code == 204
    assert update.headers["Content-Location"]

    # Read it back
    get = client.get(update.headers["Content-Location"])
    assert get.status_code == 200
    assert get.json()["description"] is None
    assert get.json()["value"] == "test"


def test_update_observable_type_multiple_fields(client):
    # Create an observable type
    create = client.post("/api/observable/type/", json={"value": "default"})

    # Update multiple fields
    update = client.put(
        create.headers["Content-Location"],
        json={"description": "Test", "value": "test"},
    )
    assert update.status_code == 204
    assert update.headers["Content-Location"]

    # Read it back
    get = client.get(update.headers["Content-Location"])
    assert get.status_code == 200
    assert get.json()["description"] == "Test"
    assert get.json()["value"] == "test"


def test_udpate_observable_type_same_value(client):
    # Create an observable type
    create = client.post("/api/observable/type/", json={"value": "default"})

    # Update a field to the same value
    update = client.put(create.headers["Content-Location"], json={"value": "default"})
    assert update.status_code == 204
    assert update.headers["Content-Location"]

    # Read it back
    get = client.get(update.headers["Content-Location"])
    assert get.status_code == 200
    assert get.json()["description"] is None
    assert get.json()["value"] == "default"


def test_update_observable_type_duplicate_value(client):
    # Create some observable types
    client.post("/api/observable/type/", json={"value": "default"})
    create = client.post("/api/observable/type/", json={"value": "intel"})

    # Ensure you cannot update an observable type value to one that already exists
    update = client.put(create.headers["Content-Location"], json={"value": "default"})
    assert update.status_code == 400


def test_update_observable_type_invalid_uuid(client):
    update = client.put("/api/observable/type/1", json={"value": "default"})
    assert update.status_code == 422


def test_update_observable_type_invalid_value(client):
    update = client.put(f"/api/observable/type/{uuid.uuid4()}", json={"value": {"asdf": "asdf"}})
    assert update.status_code == 422


def test_update_observable_type_none_value(client):
    # Create an observable type
    create = client.post("/api/observable/type/", json={"value": "default"})

    # Ensure you cannot update an observable type value to None
    update = client.put(create.headers["Content-Location"], json={"value": None})
    assert update.status_code == 422


def test_update_nonexistent_observable_type(client):
    update = client.put(f"/api/observable/type/{uuid.uuid4()}", json={"value": "default"})
    assert update.status_code == 404


#
# DELETE
#


def test_delete_observable_type(client):
    # Create an observable type
    create = client.post("/api/observable/type/", json={"value": "default"})

    # Delete it
    delete = client.delete(create.headers["Content-Location"])
    assert delete.status_code == 204

    # Make sure it is gone
    get = client.get(create.headers["Content-Location"])
    assert get.status_code == 404


def test_delete_invalid_observable_type(client):
    delete = client.delete("/api/observable/type/1")
    assert delete.status_code == 422


def test_delete_nonexistent_observable_type(client):
    delete = client.delete(f"/api/observable/type/{uuid.uuid4()}")
    assert delete.status_code == 400
