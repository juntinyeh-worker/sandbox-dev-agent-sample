ITEM = {"sku": "SKU-001", "name": "Widget", "price": 9.99}


def _create(client, data=None):
    return client.post("/api/inventory/", json=data or ITEM)


class TestCreateItem:
    def test_success(self, client):
        resp = _create(client)
        assert resp.status_code == 201
        body = resp.get_json()
        assert body["sku"] == ITEM["sku"]
        assert body["name"] == ITEM["name"]
        assert body["quantity"] == 0

    def test_with_optional_fields(self, client):
        resp = _create(client, {**ITEM, "quantity": 5, "category": "tools"})
        body = resp.get_json()
        assert body["quantity"] == 5
        assert body["category"] == "tools"

    def test_missing_fields(self, client):
        assert client.post("/api/inventory/", json={}).status_code == 400
        assert client.post("/api/inventory/", json={"sku": "X", "name": "Y"}).status_code == 400

    def test_duplicate_sku(self, client):
        _create(client)
        assert _create(client).status_code == 409


class TestListItems:
    def test_empty(self, client):
        assert client.get("/api/inventory/").get_json() == []

    def test_returns_all(self, client):
        _create(client, {"sku": "A", "name": "A", "price": 1})
        _create(client, {"sku": "B", "name": "B", "price": 2})
        assert len(client.get("/api/inventory/").get_json()) == 2

    def test_filter_by_category(self, client):
        _create(client, {"sku": "A", "name": "A", "price": 1, "category": "tools"})
        _create(client, {"sku": "B", "name": "B", "price": 2, "category": "parts"})
        _create(client, {"sku": "C", "name": "C", "price": 3, "category": "tools"})
        result = client.get("/api/inventory/?category=tools").get_json()
        assert len(result) == 2
        assert all(i["category"] == "tools" for i in result)

    def test_filter_no_match(self, client):
        _create(client)
        assert client.get("/api/inventory/?category=nope").get_json() == []


class TestGetItem:
    def test_found(self, client):
        iid = _create(client).get_json()["id"]
        resp = client.get(f"/api/inventory/{iid}")
        assert resp.status_code == 200
        assert resp.get_json()["sku"] == ITEM["sku"]

    def test_not_found(self, client):
        assert client.get("/api/inventory/999").status_code == 404


class TestUpdateItem:
    def test_update_fields(self, client):
        iid = _create(client).get_json()["id"]
        resp = client.put(f"/api/inventory/{iid}", json={"quantity": 10, "price": 19.99})
        assert resp.status_code == 200
        body = resp.get_json()
        assert body["quantity"] == 10
        assert body["price"] == "19.99"

    def test_not_found(self, client):
        assert client.put("/api/inventory/999", json={"quantity": 1}).status_code == 404


class TestDeleteItem:
    def test_success(self, client):
        iid = _create(client).get_json()["id"]
        assert client.delete(f"/api/inventory/{iid}").status_code == 204
        assert client.get(f"/api/inventory/{iid}").status_code == 404

    def test_not_found(self, client):
        assert client.delete("/api/inventory/999").status_code == 404
