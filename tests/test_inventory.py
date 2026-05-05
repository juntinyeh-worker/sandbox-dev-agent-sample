def test_list_items_empty(client):
    resp = client.get("/api/inventory/")
    assert resp.status_code == 200
    assert resp.get_json() == []


def test_create_item(client):
    resp = client.post("/api/inventory/", json={"sku": "A1", "name": "Widget", "price": 9.99})
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["sku"] == "A1"
    assert data["quantity"] == 0


def test_create_item_missing_fields(client):
    resp = client.post("/api/inventory/", json={"sku": "A1", "name": "Widget"})
    assert resp.status_code == 400


def test_create_item_duplicate_sku(client):
    client.post("/api/inventory/", json={"sku": "A1", "name": "Widget", "price": 9.99})
    resp = client.post("/api/inventory/", json={"sku": "A1", "name": "Other", "price": 1.00})
    assert resp.status_code == 409


def test_get_item(client):
    r = client.post("/api/inventory/", json={"sku": "A1", "name": "Widget", "price": 9.99})
    iid = r.get_json()["id"]
    resp = client.get(f"/api/inventory/{iid}")
    assert resp.status_code == 200
    assert resp.get_json()["name"] == "Widget"


def test_get_item_not_found(client):
    resp = client.get("/api/inventory/999")
    assert resp.status_code == 404


def test_update_item(client):
    r = client.post("/api/inventory/", json={"sku": "A1", "name": "Widget", "price": 9.99})
    iid = r.get_json()["id"]
    resp = client.put(f"/api/inventory/{iid}", json={"quantity": 10, "category": "tools"})
    assert resp.status_code == 200
    assert resp.get_json()["quantity"] == 10
    assert resp.get_json()["category"] == "tools"


def test_delete_item(client):
    r = client.post("/api/inventory/", json={"sku": "A1", "name": "Widget", "price": 9.99})
    iid = r.get_json()["id"]
    resp = client.delete(f"/api/inventory/{iid}")
    assert resp.status_code == 204
    assert client.get(f"/api/inventory/{iid}").status_code == 404


def test_list_items_filter_category(client):
    client.post("/api/inventory/", json={"sku": "A1", "name": "W1", "price": 1, "category": "tools"})
    client.post("/api/inventory/", json={"sku": "A2", "name": "W2", "price": 2, "category": "food"})
    resp = client.get("/api/inventory/?category=tools")
    data = resp.get_json()
    assert len(data) == 1
    assert data[0]["category"] == "tools"
