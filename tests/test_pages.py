def test_create_page(client, auth_header):
    r = client.post("/api/pages/", json={"name": "Dashboard"}, headers=auth_header)
    assert r.status_code == 201
    assert r.json()["name"] == "Dashboard"


def test_list_pages(client, auth_header):
    client.post("/api/pages/", json={"name": "Sales"}, headers=auth_header)
    client.post("/api/pages/", json={"name": "Marketing"}, headers=auth_header)
    pages = client.get("/api/pages/", headers=auth_header).json()
    assert len(pages) == 2


def test_get_single_page(client, auth_header):
    created = client.post("/api/pages/", json={"name": "My Page"}, headers=auth_header).json()
    r = client.get(f"/api/pages/{created['id']}", headers=auth_header)
    assert r.status_code == 200
    assert r.json()["name"] == "My Page"


def test_rename_page(client, auth_header):
    page = client.post("/api/pages/", json={"name": "Old Name"}, headers=auth_header).json()
    updated = client.put(f"/api/pages/{page['id']}", json={"name": "New Name"}, headers=auth_header)
    assert updated.status_code == 200
    assert updated.json()["name"] == "New Name"


def test_delete_page(client, auth_header):
    page = client.post("/api/pages/", json={"name": "Throwaway"}, headers=auth_header).json()
    assert client.delete(f"/api/pages/{page['id']}", headers=auth_header).status_code == 204
    assert client.get(f"/api/pages/{page['id']}", headers=auth_header).status_code == 404


def test_page_not_found(client, auth_header):
    assert client.get("/api/pages/9999", headers=auth_header).status_code == 404


def test_pages_require_login(client):
    assert client.get("/api/pages/").status_code == 403
