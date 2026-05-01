def test_register(client):
    r = client.post("/api/users/register", json={"username": "alice", "password": "secret123"})
    assert r.status_code == 201
    body = r.json()
    assert body["username"] == "alice"
    assert "id" in body


def test_cant_register_twice(client):
    payload = {"username": "bob", "password": "secret123"}
    client.post("/api/users/register", json=payload)
    assert client.post("/api/users/register", json=payload).status_code == 409


def test_login_and_get_token(client):
    client.post("/api/users/register", json={"username": "charlie", "password": "mypass"})
    r = client.post("/api/users/login", json={"username": "charlie", "password": "mypass"})
    assert r.status_code == 200
    assert "access_token" in r.json()


def test_wrong_password(client):
    client.post("/api/users/register", json={"username": "dave", "password": "rightpass"})
    r = client.post("/api/users/login", json={"username": "dave", "password": "nope"})
    assert r.status_code == 401


def test_me_endpoint(client, auth_header):
    resp = client.get("/api/users/me", headers=auth_header)
    assert resp.status_code == 200
    assert resp.json()["username"] == "testuser"


def test_me_rejects_anonymous(client):
    assert client.get("/api/users/me").status_code == 403
