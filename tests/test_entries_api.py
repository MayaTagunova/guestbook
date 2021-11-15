import datetime
import urllib.parse

from app.core.schemas.entry import EntryInCreate


def test_post_entry(app_client):
    response = app_client.post(
        "/entries/",
        data=EntryInCreate(title="Test title", body="Test body").json()
    )
    assert response.status_code == 201

    entry = response.json()
    assert "id" in entry
    assert "title" in entry
    assert "body" in entry
    assert "created" in entry

    response = app_client.get(
        f"/entries/{entry['id']}",
    )
    assert response.status_code == 200
    assert response.json()["id"] == entry["id"]
    assert response.json()["title"] == entry["title"]
    assert response.json()["body"] == entry["body"]
    assert response.json()["created"] == entry["created"]


def test_get_entries(app_client):
    response = app_client.get("/entries/")
    assert response.status_code == 200


def test_get_entry_by_date(app_client):
    response = app_client.post(
        "/entries/",
        data=EntryInCreate(title="Test title", body="Test body").json()
    )
    assert response.status_code == 201

    entry = response.json()
    created = datetime.datetime.fromisoformat(entry["created"])

    past_date = created - datetime.timedelta(days=1)
    future_date = created + datetime.timedelta(days=1)

    response = app_client.get(
        f"/entries/?dateFrom={urllib.parse.quote(created.isoformat())}",
    )
    assert response.status_code == 200
    ids = [item["id"] for item in response.json()["items"]]
    assert entry["id"] in ids

    response = app_client.get(
        f"/entries/?dateTo={urllib.parse.quote(created.isoformat())}",
    )
    assert response.status_code == 200
    ids = [item["id"] for item in response.json()["items"]]
    assert entry["id"] in ids

    response = app_client.get(
        f"/entries/?dateFrom={urllib.parse.quote(future_date.isoformat())}",
    )
    assert response.status_code == 200
    ids = [item["id"] for item in response.json()["items"]]
    assert entry["id"] not in ids

    response = app_client.get(
        f"/entries/?dateTo={urllib.parse.quote(past_date.isoformat())}",
    )
    assert response.status_code == 200
    ids = [item["id"] for item in response.json()["items"]]
    assert entry["id"] not in ids
