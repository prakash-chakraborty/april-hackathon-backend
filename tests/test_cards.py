def make_page(client, auth_header):
    resp = client.post("/api/pages/", json={"name": "Test Page"}, headers=auth_header)
    return resp.json()["id"]


SAMPLE_CARD = {
    "title": "Revenue",
    "card_type": "kpi",
    "metric_title": "Total Revenue",
    "metric_value": "£120k",
}


def test_create_card(client, auth_header):
    pid = make_page(client, auth_header)
    resp = client.post(f"/api/cards/?page_id={pid}", json=SAMPLE_CARD, headers=auth_header)
    assert resp.status_code == 201
    assert resp.json()["title"] == "Revenue"
    assert resp.json()["page_id"] == pid


def test_list_cards(client, auth_header):
    pid = make_page(client, auth_header)
    client.post(f"/api/cards/?page_id={pid}", json=SAMPLE_CARD, headers=auth_header)
    client.post(f"/api/cards/?page_id={pid}", json={
        "title": "Users", "card_type": "kpi",
        "metric_title": "Active Users", "metric_value": "340",
    }, headers=auth_header)

    resp = client.get(f"/api/cards/?page_id={pid}", headers=auth_header)
    assert len(resp.json()) == 2


def test_get_card(client, auth_header):
    pid = make_page(client, auth_header)
    r = client.post(f"/api/cards/?page_id={pid}", json=SAMPLE_CARD, headers=auth_header)

    resp = client.get(f"/api/cards/{r.json()['id']}", headers=auth_header)
    assert resp.status_code == 200
    assert resp.json()["metric_value"] == "£120k"


def test_update_card(client, auth_header):
    pid = make_page(client, auth_header)
    r = client.post(f"/api/cards/?page_id={pid}", json=SAMPLE_CARD, headers=auth_header)
    card_id = r.json()["id"]

    resp = client.put(f"/api/cards/{card_id}", json={"metric_value": "£200k"}, headers=auth_header)
    assert resp.json()["metric_value"] == "£200k"
    assert resp.json()["title"] == "Revenue"  # should not change


def test_delete_card(client, auth_header):
    pid = make_page(client, auth_header)
    r = client.post(f"/api/cards/?page_id={pid}", json=SAMPLE_CARD, headers=auth_header)
    card_id = r.json()["id"]

    assert client.delete(f"/api/cards/{card_id}", headers=auth_header).status_code == 204
    assert client.get(f"/api/cards/{card_id}", headers=auth_header).status_code == 404


def test_card_on_nonexistent_page(client, auth_header):
    resp = client.post("/api/cards/?page_id=9999", json=SAMPLE_CARD, headers=auth_header)
    assert resp.status_code == 404


def test_cards_need_auth(client):
    assert client.get("/api/cards/").status_code == 403


def test_cascade_delete(client, auth_header):
    """deleting a page should also remove its cards"""
    pid = make_page(client, auth_header)
    r = client.post(f"/api/cards/?page_id={pid}", json=SAMPLE_CARD, headers=auth_header)
    card_id = r.json()["id"]

    client.delete(f"/api/pages/{pid}", headers=auth_header)
    assert client.get(f"/api/cards/{card_id}", headers=auth_header).status_code == 404
