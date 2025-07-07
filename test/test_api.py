import pytest
from fastapi.testclient import TestClient
from uuid import uuid4

from backend.app import app

client = TestClient(app)

@pytest.fixture
def token():
    username = "test2"
    password = "test2"
    res = client.post(
        "/auth/register",
        json={"username": username, "password": password}
    )
    assert res.status_code == 200
    res = client.post(
        "/auth/login",
        json={"username": username, "password": password}
    )
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data
    return data["access_token"]

def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}

def test_session(token):
    headers = auth_headers(token)
    res = client.post("/api/sessions", headers=headers)
    assert res.status_code == 200
    ss = res.json()
    assert "id" in ss and "title" in ss and isinstance(ss["messages"], list)
    session_id = ss["id"]
    res = client.get("/api/sessions", headers=headers)
    assert res.status_code == 200
    all_sessions = res.json()
    assert any(s["id"] == session_id for s in all_sessions)
    res = client.get(f"/api/sessions/{session_id}", headers=headers)
    assert res.status_code == 200
    single = res.json()
    assert single["id"] == session_id
    res = client.delete(f"/api/sessions/{session_id}", headers=headers)
    assert res.status_code == 204
    res = client.get(f"/api/sessions/{session_id}", headers=headers)
    assert res.status_code == 404
