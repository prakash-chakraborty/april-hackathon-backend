CARD_DATA = {
    "title": "Revenue",
    "card_type": "kpi",
    "metric_title": "Total Revenue",
    "metric_value": "£120k",
}


def _create_page(client, headers):
    return client.post("/api/pages/", json={"name": "Test Page"}, headers=headers).json()["id"]


def test_create_card(client, auth_header):
    page_id = _create_page(client, auth_header)
    r = client.post(f"/api/cards/?page_id={page_id}", json=CARD_DATA, headers=auth_header)
    assert r.status_code == 201
    assert r.json()["title"] == "Revenue"
    assert r.json()["page_id"] == page_id


def test_list_cards_for_page(client, auth_header):
    page_id = _create_page(client, auth_header)
    client.post(f"/api/cards/?page_id={page_id}", json=CARD_DATA, headers=auth_header)
    client.post(f"/api/cards/?page_id={page_id}", json={
        "title": "Users", "card_type": "kpi",
        "metric_title": "Active Users", "metric_value": "340",
    }, headers=auth_header)
    cards = client.get(f"/api/cards/?page_id={page_id}", headers=auth_header).json()
    assert len(cards) == 2


def test_fetch_single_card(client, auth_header):
    page_id = _create_page(client, auth_header)
    created = client.post(f"/api/cards/?page_id={page_id}", json=CARD_DATA, headers=auth_header).json()

    r = client.get(f"/api/cards/{created['id']}", headers=auth_header)
    assert r.status_code == 200
    assert r.json()["metric_value"] == "£120k"


def test_partial_update(client, auth_header):
    page_id = _create_page(client, auth_header)
    card = client.post(f"/api/cards/?page_id={page_id}", json=CARD_DATA, headers=auth_header).json()

    updated = client.put(
        f"/api/cards/{card['id']}",
        json={"metric_value": "£200k"},
        headers=auth_header,
    ).json()
    assert updated["metric_value"] == "£200k"
    assert updated["title"] == "Revenue"


def test_delete_card(client, auth_header):
    page_id = _create_page(client, auth_header)
    card = client.post(f"/api/cards/?page_id={page_id}", json=CARD_DATA, headers=auth_header).json()

    assert client.delete(f"/api/cards/{card['id']}", headers=auth_header).status_code == 204
    assert client.get(f"/api/cards/{card['id']}", headers=auth_header).status_code == 404


def test_cant_add_card_to_missing_page(client, auth_header):
    r = client.post("/api/cards/?page_id=9999", json=CARD_DATA, headers=auth_header)
    assert r.status_code == 404


def test_cards_require_auth(client):
    assert client.get("/api/cards/").status_code == 403


def test_deleting_page_removes_its_cards(client, auth_header):
    page_id = _create_page(client, auth_header)
    card = client.post(f"/api/cards/?page_id={page_id}", json=CARD_DATA, headers=auth_header).json()

    client.delete(f"/api/pages/{page_id}", headers=auth_header)
    assert client.get(f"/api/cards/{card['id']}", headers=auth_header).status_code == 404
