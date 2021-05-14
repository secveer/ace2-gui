"""
NOTE: There are no tests for the foreign key constraints, namely deleting a Disposition that is tied to and Alert.
The DELETE endpoint will need to be updated once the Alert endpoints are in place in order to account for this.
"""


#
# CREATE
#


def test_create_disposition(client):
    # Create a disposition
    create = client.post("/api/disposition", json={"rank": 1, "value": "FALSE_POSITIVE"})
    assert create.status_code == 201
    assert create.json() is True
    assert create.headers["Location"]

    # Make sure it can be read back
    get = client.get(create.headers["Location"])
    assert get.status_code == 200
    assert get.json()["description"] is None
    assert get.json()["rank"] == 1
    assert get.json()["value"] == "FALSE_POSITIVE"


def test_create_disposition_duplicate_rank(client):
    # Create a disposition
    client.post("/api/disposition", json={"rank": 1, "value": "FALSE_POSITIVE"})

    # Ensure you cannot create another disposition with the same rank
    create = client.post("/api/disposition", json={"rank": 1, "value": "IGNORE"})
    assert create.status_code == 409


def test_create_disposition_duplicate_value(client):
    # Create a disposition
    client.post("/api/disposition", json={"rank": 1, "value": "FALSE_POSITIVE"})

    # Ensure you cannot create another disposition with the same value
    create = client.post("/api/disposition", json={"rank": 2, "value": "FALSE_POSITIVE"})
    assert create.status_code == 409


def test_create_disposition_missing_rank(client):
    create = client.post("/api/disposition", json={"value": "FALSE_POSITIVE"})
    assert create.status_code == 422


def test_create_disposition_missing_value(client):
    create = client.post("/api/disposition", json={"rank": 1})
    assert create.status_code == 422


#
# READ
#


def test_get_all_dispositions(client):
    # There should not be any dispositions at first
    get = client.get("/api/disposition")
    assert get.status_code == 200
    assert get.json() == []

    # Create some dispositions
    client.post("/api/disposition", json={"rank": 1, "value": "FALSE_POSITIVE"})
    client.post("/api/disposition", json={"rank": 2, "value": "IGNORE"})
    
    # Read them back
    get = client.get("/api/disposition")
    assert get.status_code == 200
    assert len(get.json()) == 2


def test_get_nonexistent_disposition(client):
    get = client.get("/api/disposition/1")
    assert get.status_code == 404


#
# UPDATE
#


def test_update_disposition(client):
    # Create a disposition
    create = client.post("/api/disposition", json={"rank": 1, "value": "FALSE_POSITIVE"})

    # Update a single field
    update = client.put(create.headers["Location"], json={"rank": "3"})
    assert update.status_code == 200
    assert update.json() is True
    assert update.headers["Location"]

    # Update multiple fields
    update = client.put(create.headers["Location"], json={"value": "UPDATED", "description": "Test"})
    assert update.status_code == 200
    assert update.json() is True
    assert update.headers["Location"]

    # Update a field to the same value
    update = client.put(create.headers["Location"], json={"rank": "3"})
    assert update.status_code == 200
    assert update.json() is True
    assert update.headers["Location"]

    # Read it back to make sure the update was successful
    get = client.get(update.headers["Location"])
    assert get.status_code == 200
    assert get.json()["description"] == "Test"
    assert get.json()["rank"] == 3
    assert get.json()["value"] == "UPDATED"


def test_update_disposition_duplicate_rank(client):
    # Create some dispositions
    client.post("/api/disposition", json={"rank": 1, "value": "FALSE_POSITIVE"})
    create = client.post("/api/disposition", json={"rank": 2, "value": "IGNORE"})

    # Ensure you cannot update a disposition rank to one that already exists
    update = client.put(create.headers["Location"], json={"rank": 1})
    assert update.status_code == 400


def test_update_disposition_duplicate_value(client):
    # Create some dispositions
    client.post("/api/disposition", json={"rank": 1, "value": "FALSE_POSITIVE"})
    create = client.post("/api/disposition", json={"rank": 2, "value": "IGNORE"})

    # Ensure you cannot update a disposition rank to one that already exists
    update = client.put(create.headers["Location"], json={"value": "FALSE_POSITIVE"})
    assert update.status_code == 400


def test_update_disposition_none_rank(client):
    # Create a disposition
    create = client.post("/api/disposition", json={"rank": 1, "value": "FALSE_POSITIVE"})

    # Ensure you cannot update a disposition rank to None
    update = client.put(create.headers["Location"], json={"rank": None})
    assert update.status_code == 400


def test_update_disposition_none_value(client):
    # Create a disposition
    create = client.post("/api/disposition", json={"rank": 1, "value": "FALSE_POSITIVE"})

    # Ensure you cannot update a disposition value to None
    update = client.put(create.headers["Location"], json={"value": None})
    assert update.status_code == 400


def test_update_nonexistent_disposition(client):
    update = client.put("/api/disposition/1", json={"value": "FALSE_POSITIVE"})
    assert update.status_code == 404


#
# DELETE
#


def test_delete_disposition(client):
    # Create a disposition
    create = client.post("/api/disposition", json={"rank": 1, "value": "FALSE_POSITIVE"})

    # Delete it
    delete = client.delete(create.headers["Location"])
    assert delete.status_code == 200
    assert delete.json() is True

    # Make sure it is gone
    get = client.get(create.headers["Location"])
    assert get.status_code == 404


def test_delete_nonexistent_disposition(client):
    delete = client.delete("/api/disposition/1")
    assert delete.status_code == 400