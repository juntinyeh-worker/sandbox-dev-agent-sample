import pytest


MEMBER = {"email": "a@b.com", "name": "Alice"}


def _create(client, data=None):
    return client.post("/api/members/", json=data or MEMBER)


class TestCreateMember:
    def test_success(self, client):
        resp = _create(client)
        assert resp.status_code == 201
        body = resp.get_json()
        assert body["email"] == MEMBER["email"]
        assert body["name"] == MEMBER["name"]
        assert body["tier"] == "basic"
        assert body["active"] is True

    def test_custom_tier(self, client):
        resp = _create(client, {**MEMBER, "tier": "vip"})
        assert resp.get_json()["tier"] == "vip"

    def test_missing_fields(self, client):
        assert client.post("/api/members/", json={}).status_code == 400
        assert client.post("/api/members/", json={"email": "x"}).status_code == 400
        assert client.post("/api/members/", json={"name": "x"}).status_code == 400

    def test_duplicate_email(self, client):
        _create(client)
        assert _create(client).status_code == 409


class TestListMembers:
    def test_empty(self, client):
        assert client.get("/api/members/").get_json() == []

    def test_returns_all(self, client):
        _create(client, {"email": "a@b.com", "name": "A"})
        _create(client, {"email": "b@b.com", "name": "B"})
        assert len(client.get("/api/members/").get_json()) == 2


class TestGetMember:
    def test_found(self, client):
        mid = _create(client).get_json()["id"]
        resp = client.get(f"/api/members/{mid}")
        assert resp.status_code == 200
        assert resp.get_json()["email"] == MEMBER["email"]

    def test_not_found(self, client):
        assert client.get("/api/members/999").status_code == 404


class TestUpdateMember:
    def test_update_fields(self, client):
        mid = _create(client).get_json()["id"]
        resp = client.put(f"/api/members/{mid}", json={"name": "Bob", "tier": "premium"})
        assert resp.status_code == 200
        body = resp.get_json()
        assert body["name"] == "Bob"
        assert body["tier"] == "premium"

    def test_not_found(self, client):
        assert client.put("/api/members/999", json={"name": "X"}).status_code == 404


class TestDeleteMember:
    def test_success(self, client):
        mid = _create(client).get_json()["id"]
        assert client.delete(f"/api/members/{mid}").status_code == 204
        assert client.get(f"/api/members/{mid}").status_code == 404

    def test_not_found(self, client):
        assert client.delete("/api/members/999").status_code == 404
