def test_create_page(client, auth_header):
    resp = client.post("/api/pages/", json={"name": "Dashboard"}, headers=auth_header)
    assert resp.status_code == 201
    assert resp.json()["name"] == "Dashboard"


def test_list_pages(client, auth_header):
    client.post("/api/pages/", json={"name": "Page A"}, headers=auth_header)
    client.post("/api/pages/", json={"name": "Page B"}, headers=auth_header)
    resp = client.get("/api/pages/", headers=auth_header)
    assert len(resp.json()) == 2


def test_get_page(client, auth_header):
    r = client.post("/api/pages/", json={"name": "My Page"}, headers=auth_header)
    page_id = r.json()["id"]
    resp = client.get(f"/api/pages/{page_id}", headers=auth_header)
    assert resp.status_code == 200
    assert resp.json()["name"] == "My Page"


def test_update_page(client, auth_header):
    r = client.post("/api/pages/", json={"name": "Old Name"}, headers=auth_header)
    resp = client.put(f"/api/pages/{r.json()['id']}", json={"name": "New Name"}, headers=auth_header)
    assert resp.status_code == 200
    assert resp.json()["name"] == "New Name"


def test_delete_page(client, auth_header):
    r = client.post("/api/pages/", json={"name": "Temp"}, headers=auth_header)
    page_id = r.json()["id"]
    assert client.delete(f"/api/pages/{page_id}", headers=auth_header).status_code == 204
    # should be gone now
    assert client.get(f"/api/pages/{page_id}", headers=auth_header).status_code == 404


def test_page_404(client, auth_header):
    assert client.get("/api/pages/9999", headers=auth_header).status_code == 404


def test_pages_need_auth(client):
    assert client.get("/api/pages/").status_code == 403
