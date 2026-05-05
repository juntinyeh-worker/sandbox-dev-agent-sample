def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "healthy"


def test_list_members_empty(client):
    resp = client.get("/api/members/")
    assert resp.status_code == 200
    assert resp.get_json() == []


def test_create_member(client):
    resp = client.post("/api/members/", json={"email": "a@b.com", "name": "A"})
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["email"] == "a@b.com"
    assert data["tier"] == "basic"


def test_create_member_missing_fields(client):
    resp = client.post("/api/members/", json={"email": "a@b.com"})
    assert resp.status_code == 400


def test_create_member_duplicate(client):
    client.post("/api/members/", json={"email": "a@b.com", "name": "A"})
    resp = client.post("/api/members/", json={"email": "a@b.com", "name": "B"})
    assert resp.status_code == 409


def test_get_member(client):
    r = client.post("/api/members/", json={"email": "a@b.com", "name": "A"})
    mid = r.get_json()["id"]
    resp = client.get(f"/api/members/{mid}")
    assert resp.status_code == 200
    assert resp.get_json()["name"] == "A"


def test_get_member_not_found(client):
    resp = client.get("/api/members/999")
    assert resp.status_code == 404


def test_update_member(client):
    r = client.post("/api/members/", json={"email": "a@b.com", "name": "A"})
    mid = r.get_json()["id"]
    resp = client.put(f"/api/members/{mid}", json={"name": "B", "tier": "vip"})
    assert resp.status_code == 200
    assert resp.get_json()["name"] == "B"
    assert resp.get_json()["tier"] == "vip"


def test_delete_member(client):
    r = client.post("/api/members/", json={"email": "a@b.com", "name": "A"})
    mid = r.get_json()["id"]
    resp = client.delete(f"/api/members/{mid}")
    assert resp.status_code == 204
    assert client.get(f"/api/members/{mid}").status_code == 404
