import uuid


"""
NOTE: There are no tests for the foreign key constraints, namely deleting an UserRole that is tied to a User.
The DELETE endpoint will need to be updated once the User endpoints are in place in order to account for this.
"""


#
# CREATE
#


def test_create_user_role(client):
    # Create a user role
    create = client.post("/api/user/role/", json={"value": "default"})
    assert create.status_code == 201
    assert create.headers["Content-Location"]

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert get.status_code == 200
    assert get.json()["description"] is None
    assert get.json()["value"] == "default"


def test_create_user_role_with_uuid(client):
    # Create a user role and specify the UUID it should use
    u = str(uuid.uuid4())
    create = client.post("/api/user/role/", json={"uuid": u, "value": "default"})
    assert create.status_code == 201
    assert create.headers["Content-Location"]

    # Read it back using the UUID
    get = client.get(f"/api/user/role/{u}")
    assert get.status_code == 200
    assert get.json()["uuid"] == u
    assert get.json()["description"] is None
    assert get.json()["value"] == "default"


def test_create_user_role_duplicate_value(client):
    # Create a user role
    client.post("/api/user/role/", json={"value": "default"})

    # Ensure you cannot create another user role with the same value
    create = client.post("/api/user/role/", json={"value": "default"})
    assert create.status_code == 409


def test_create_user_role_invalid_uuid(client):
    create = client.post("/api/user/role/", json={"uuid": 1, "value": "default"})
    assert create.status_code == 422


def test_create_user_role_invalid_value(client):
    create = client.post("/api/user/role/", json={"value": {"asdf": "asdf"}})
    assert create.status_code == 422


def test_create_user_role_missing_value(client):
    create = client.post("/api/user/role/", json={})
    assert create.status_code == 422


#
# READ
#


def test_get_all_user_roles(client):
    # Create some user roles
    client.post("/api/user/role/", json={"value": "default"})
    client.post("/api/user/role/", json={"value": "intel"})

    # Read them back
    get = client.get("/api/user/role/")
    assert get.status_code == 200
    assert len(get.json()) == 2


def test_get_all_user_roles_empty(client):
    get = client.get("/api/user/role/")
    assert get.status_code == 200
    assert get.json() == []


def test_get_invalid_user_role(client):
    get = client.get("/api/user/role/1")
    assert get.status_code == 422


def test_get_nonexistent_user_role(client):
    get = client.get(f"/api/user/role/{uuid.uuid4()}")
    assert get.status_code == 404


#
# UPDATE
#


def test_update_user_role(client):
    # Create a user role
    create = client.post("/api/user/role/", json={"value": "default"})

    # Update a single field
    update = client.put(create.headers["Content-Location"], json={"value": "test"})
    assert update.status_code == 204
    assert update.headers["Content-Location"]

    # Read it back
    get = client.get(update.headers["Content-Location"])
    assert get.status_code == 200
    assert get.json()["description"] is None
    assert get.json()["value"] == "test"


def test_update_user_role_multiple_fields(client):
    # Create a user role
    create = client.post("/api/user/role/", json={"value": "default"})

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


def test_udpate_user_role_same_value(client):
    # Create a user role
    create = client.post("/api/user/role/", json={"value": "default"})

    # Update a field to the same value
    update = client.put(create.headers["Content-Location"], json={"value": "default"})
    assert update.status_code == 204
    assert update.headers["Content-Location"]

    # Read it back
    get = client.get(update.headers["Content-Location"])
    assert get.status_code == 200
    assert get.json()["description"] is None
    assert get.json()["value"] == "default"


def test_update_user_role_duplicate_value(client):
    # Create some user roles
    client.post("/api/user/role/", json={"value": "default"})
    create = client.post("/api/user/role/", json={"value": "intel"})

    # Ensure you cannot update a user role value to one that already exists
    update = client.put(create.headers["Content-Location"], json={"value": "default"})
    assert update.status_code == 400


def test_update_user_role_invalid_uuid(client):
    update = client.put("/api/user/role/1", json={"value": "default"})
    assert update.status_code == 422


def test_update_user_role_invalid_value(client):
    update = client.put(f"/api/user/role/{uuid.uuid4()}", json={"value": {"asdf": "asdf"}})
    assert update.status_code == 422


def test_update_user_role_none_value(client):
    # Create a user role
    create = client.post("/api/user/role/", json={"value": "default"})

    # Ensure you cannot update a user role value to None
    update = client.put(create.headers["Content-Location"], json={"value": None})
    assert update.status_code == 400


def test_update_nonexistent_user_role(client):
    update = client.put(f"/api/user/role/{uuid.uuid4()}", json={"value": "default"})
    assert update.status_code == 404


#
# DELETE
#


def test_delete_user_role(client):
    # Create a user role
    create = client.post("/api/user/role/", json={"value": "default"})

    # Delete it
    delete = client.delete(create.headers["Content-Location"])
    assert delete.status_code == 204

    # Make sure it is gone
    get = client.get(create.headers["Content-Location"])
    assert get.status_code == 404


def test_delete_invalid_user_role(client):
    delete = client.delete("/api/user/role/1")
    assert delete.status_code == 422


def test_delete_nonexistent_user_role(client):
    delete = client.delete(f"/api/user/role/{uuid.uuid4()}")
    assert delete.status_code == 400
