def test_register(client):
    resp = client.post("/api/users/register", json={"username": "alice", "password": "secret123"})
    assert resp.status_code == 201
    assert resp.json()["username"] == "alice"
    assert "id" in resp.json()


def test_register_duplicate(client):
    client.post("/api/users/register", json={"username": "bob", "password": "secret123"})
    resp = client.post("/api/users/register", json={"username": "bob", "password": "other456"})
    assert resp.status_code == 409


def test_login(client):
    client.post("/api/users/register", json={"username": "charlie", "password": "mypass"})
    resp = client.post("/api/users/login", json={"username": "charlie", "password": "mypass"})
    assert resp.status_code == 200
    assert "access_token" in resp.json()


def test_login_bad_password(client):
    client.post("/api/users/register", json={"username": "dave", "password": "rightpass"})
    resp = client.post("/api/users/login", json={"username": "dave", "password": "wrongpass"})
    assert resp.status_code == 401


def test_get_me(client, auth_header):
    resp = client.get("/api/users/me", headers=auth_header)
    assert resp.status_code == 200
    assert resp.json()["username"] == "testuser"


def test_me_without_token(client):
    resp = client.get("/api/users/me")
    assert resp.status_code == 403
