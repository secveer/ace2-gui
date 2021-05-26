import uuid


"""
NOTE: There are no tests for the foreign key constraints, namely deleting a NodeThreat that is tied to a Node.
The DELETE endpoint will need to be updated once the Node endpoints are in place in order to account for this.
"""


#
# CREATE
#


def test_create_node_threat(client):
    # Create a node threat type
    threat_type_uuid = str(uuid.uuid4())
    client.post("/api/node/threat/type/", json={"uuid": threat_type_uuid, "value": "test_type"})

    # Create a node threat using the type that was just created
    create = client.post("/api/node/threat/", json={"value": "test", "types": ["test_type"]})
    assert create.status_code == 201
    assert create.headers["Content-Location"]

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert get.status_code == 200
    assert get.json()["description"] is None
    assert get.json()["types"] == [
        {
            "description": None,
            "uuid": threat_type_uuid,
            "value": "test_type",
        },
    ]
    assert get.json()["value"] == "test"


def test_create_node_threat_with_uuid(client):
    # Create a node threat type
    threat_type_uuid = str(uuid.uuid4())
    client.post("/api/node/threat/type/", json={"uuid": threat_type_uuid, "value": "test_type"})

    # Create a node threat using the type that was just created
    threat_uuid = str(uuid.uuid4())
    create = client.post("/api/node/threat/", json={"uuid": threat_uuid, "value": "test", "types": ["test_type"]})
    assert create.status_code == 201
    assert create.headers["Content-Location"]

    # Read it back
    get = client.get(f"/api/node/threat/{threat_uuid}")
    assert get.status_code == 200
    assert get.json()["uuid"] == threat_uuid
    assert get.json()["description"] is None
    assert get.json()["types"] == [
        {
            "description": None,
            "uuid": threat_type_uuid,
            "value": "test_type",
        },
    ]
    assert get.json()["value"] == "test"


def test_create_node_threat_multiple_types(client):
    # Create some node threat types
    client.post("/api/node/threat/type/", json={"value": "test_type"})
    client.post("/api/node/threat/type/", json={"value": "test_type2"})

    # Create a node threat using the types that were just created
    create = client.post("/api/node/threat/", json={"value": "test", "types": ["test_type", "test_type2"]})
    assert create.status_code == 201

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert get.status_code == 200
    assert len(get.json()["types"]) == 2
    assert any(t["value"] == "test_type" for t in get.json()["types"])
    assert any(t["value"] == "test_type2" for t in get.json()["types"])



def test_create_node_threat_repeated_type(client):
    # Create a node threat type
    threat_type_uuid = str(uuid.uuid4())
    client.post("/api/node/threat/type/", json={"uuid": threat_type_uuid, "value": "test_type"})

    # Create a node threat using the type that was just created
    create = client.post("/api/node/threat/", json={"value": "test", "types": ["test_type", "test_type"]})
    assert create.status_code == 201
    assert create.headers["Content-Location"]

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert get.status_code == 200
    assert get.json()["description"] is None
    assert get.json()["types"] == [
        {
            "description": None,
            "uuid": threat_type_uuid,
            "value": "test_type",
        },
    ]
    assert get.json()["value"] == "test"


def test_create_node_threat_duplicate_value(client):
    # Create a node threat type
    threat_type_uuid = str(uuid.uuid4())
    client.post("/api/node/threat/type/", json={"uuid": threat_type_uuid, "value": "test_type"})

    # Create a node threat using the type that was just created
    create = client.post("/api/node/threat/", json={"value": "test", "types": ["test_type"]})
    assert create.status_code == 201
    assert create.headers["Content-Location"]

    # Ensure you cannot create another node threat with the same value
    create = client.post("/api/node/threat/", json={"value": "test", "types": ["test_type"]})
    assert create.status_code == 409


def test_create_node_threat_empty_type(client):
    create = client.post("/api/node/threat/", json={"value": "test", "types": []})
    assert create.status_code == 422


def test_create_node_threat_invalid_type(client):
    create = client.post("/api/node/threat/", json={"value": "test", "types": "test_type"})
    assert create.status_code == 422


def test_create_node_threat_invalid_uuid(client):
    create = client.post("/api/node/threat/", json={"uuid": 1, "value": "test", "types": ["test_type"]})
    assert create.status_code == 422


def test_create_node_threat_invalid_value(client):
    create = client.post("/api/node/threat/", json={"value": {"asdf": "asdf"}, "types": ["test_type"]})
    assert create.status_code == 422


def test_create_node_threat_missing_type(client):
    create = client.post("/api/node/threat/", json={"value": "test"})
    assert create.status_code == 422


def test_create_node_threat_missing_value(client):
    create = client.post("/api/node/threat/", json={"types": ["test_type"]})
    assert create.status_code == 422


def test_create_node_threat_nonexistent_type(client):
    create = client.post("/api/node/threat/", json={"value": "test", "types": ["test_type"]})
    assert create.status_code == 404


#
# READ
#


def test_get_all_node_threats(client):
    # Create a node threat type
    threat_type_uuid = str(uuid.uuid4())
    client.post("/api/node/threat/type/", json={"uuid": threat_type_uuid, "value": "test_type"})

    # Create some node threats using the type that was just created
    client.post("/api/node/threat/", json={"value": "test", "types": ["test_type"]})
    client.post("/api/node/threat/", json={"value": "test2", "types": ["test_type"]})
    
    # Read them back
    get = client.get("/api/node/threat/")
    assert get.status_code == 200
    assert len(get.json()) == 2


def test_get_all_node_threats_empty(client):
    get = client.get("/api/node/threat/")
    assert get.status_code == 200
    assert get.json() == []


def test_get_invalid_node_threat(client):
    get = client.get("/api/node/threat/1")
    assert get.status_code == 422


def test_get_nonexistent_node_threat(client):
    get = client.get(f"/api/node/threat/{uuid.uuid4()}")
    assert get.status_code == 404


#
# UPDATE
#


def test_update_node_threat(client):
    # Create a node threat type
    client.post("/api/node/threat/type/", json={"value": "test_type"})

    # Create a node threat using the type that was just created
    create = client.post("/api/node/threat/", json={"value": "test", "types": ["test_type"]})

    # Update a single field
    update = client.put(create.headers["Content-Location"], json={"value": "test_updated"})
    assert update.status_code == 204
    assert update.headers["Content-Location"]

    # Read it back
    get = client.get(update.headers["Content-Location"])
    assert get.status_code == 200
    assert get.json()["description"] is None
    assert get.json()["value"] == "test_updated"


def test_update_node_threat_multiple_fields(client):
    # Create a node threat type
    client.post("/api/node/threat/type/", json={"value": "test_type"})

    # Create a node threat using the type that was just created
    create = client.post("/api/node/threat/", json={"value": "test", "types": ["test_type"]})

    # Update a single field
    update = client.put(
        create.headers["Content-Location"],
        json={"description": "test", "value": "test_updated"})
    assert update.status_code == 204
    assert update.headers["Content-Location"]

    # Read it back
    get = client.get(update.headers["Content-Location"])
    assert get.status_code == 200
    assert get.json()["description"] == "test"
    assert get.json()["value"] == "test_updated"


def test_update_node_threat_remove_type(client):
    # Create some node threat types
    client.post("/api/node/threat/type/", json={"value": "test_type"})
    client.post("/api/node/threat/type/", json={"value": "test_type2"})

    # Create a node threat using the types that were just created
    create = client.post("/api/node/threat/", json={"value": "test", "types": ["test_type", "test_type2"]})
    assert create.status_code == 201

    # Update the node threat to remove one of the types
    update = client.put(create.headers["Content-Location"], json={"types": ["test_type"]})
    assert update.status_code == 204
    assert update.headers["Content-Location"]

    # Read it back
    get = client.get(update.headers["Content-Location"])
    assert get.status_code == 200
    assert len(get.json()["types"]) == 1
    assert get.json()["types"][0]["value"] == "test_type"


def test_update_node_threat_same_value(client):
    # Create a node threat type
    client.post("/api/node/threat/type/", json={"value": "test_type"})

    # Create a node threat using the type that was just created
    create = client.post("/api/node/threat/", json={"value": "test", "types": ["test_type"]})

    # Update a field to the same value
    update = client.put(create.headers["Content-Location"], json={"value": "test"})
    assert update.status_code == 204
    assert update.headers["Content-Location"]

    # Read it back
    get = client.get(update.headers["Content-Location"])
    assert get.status_code == 200
    assert get.json()["description"] is None
    assert get.json()["value"] == "test"


def test_update_node_threat_duplicate_value(client):
    # Create a node threat type
    client.post("/api/node/threat/type/", json={"value": "test_type"})

    # Create some node threats using the type that was just created
    client.post("/api/node/threat/", json={"value": "default", "types": ["test_type"]})
    create = client.post("/api/node/threat/", json={"value": "test", "types": ["test_type"]})

    # Ensure you cannot update a node threat type value to one that already exists
    update = client.put(create.headers["Content-Location"], json={"value": "default"})
    assert update.status_code == 400


def test_update_node_threat_empty_type(client):
    update = client.put(f"/api/node/threat/{uuid.uuid4()}", json={"types": []})
    assert update.status_code == 422


def test_update_node_threat_invalid_uuid(client):
    update = client.put("/api/node/threat/1", json={"value": "default"})
    assert update.status_code == 422


def test_update_node_threat_invalid_value(client):
    update = client.put(f"/api/node/threat/type/{uuid.uuid4()}", json={"value": {"asdf": "asdf"}})
    assert update.status_code == 422


def test_update_node_threat_none_value(client):
    # Create a node threat type
    client.post("/api/node/threat/type/", json={"value": "test_type"})

    # Create a node threat using the type that was just created
    create = client.post("/api/node/threat/", json={"value": "default", "types": ["test_type"]})

    # Ensure you cannot update a node threat value to None
    update = client.put(create.headers["Content-Location"], json={"value": None})
    assert update.status_code == 422


def test_update_nonexistent_node_threat(client):
    update = client.put(f"/api/node/threat/{uuid.uuid4()}", json={"value": "default"})
    assert update.status_code == 404


#
# DELETE
#


def test_delete_node_threat(client):
    # Create a node threat type
    type_create = client.post("/api/node/threat/type/", json={"value": "test_type"})

    # Create a node threat using the type that was just created
    create = client.post("/api/node/threat/", json={"value": "default", "types": ["test_type"]})

    # Delete it
    delete = client.delete(create.headers["Content-Location"])
    assert delete.status_code == 204

    # Make sure it is gone
    get = client.get(create.headers["Content-Location"])
    assert get.status_code == 404

    # Make sure the node threat type is still there
    get = client.get(type_create.headers["Content-Location"])
    assert get.status_code == 200
    assert get.json()["value"] == "test_type"


def test_delete_invalid_node_threat(client):
    delete = client.delete("/api/node/threat/1")
    assert delete.status_code == 422


def test_delete_nonexistent_node_threat_type(client):
    delete = client.delete(f"/api/node/threat/{uuid.uuid4()}")
    assert delete.status_code == 400