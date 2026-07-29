import pytest
from fastapi.testclient import TestClient

from app import storage
from app.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_storage():
    storage._reset()
    yield
    storage._reset()


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------

def test_health_ok():
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert "timestamp" in data


# ---------------------------------------------------------------------------
# POST /tasks – create
# ---------------------------------------------------------------------------

def test_create_task_minimal():
    resp = client.post("/tasks", json={"title": "Buy milk"})
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == "Buy milk"
    assert data["status"] == "ToDo"
    assert data["priority"] == "Medium"
    assert data["description"] == ""
    assert data["assignee"] is None
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_create_task_full():
    resp = client.post(
        "/tasks",
        json={
            "title": "Write tests",
            "description": "Cover all endpoints",
            "status": "InProgress",
            "priority": "High",
            "assignee": "alice",
        },
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == "Write tests"
    assert data["description"] == "Cover all endpoints"
    assert data["status"] == "InProgress"
    assert data["priority"] == "High"
    assert data["assignee"] == "alice"


def test_create_task_blank_title_rejected():
    resp = client.post("/tasks", json={"title": "   "})
    assert resp.status_code == 422


def test_create_task_title_too_long_rejected():
    resp = client.post("/tasks", json={"title": "x" * 201})
    assert resp.status_code == 422


def test_create_task_invalid_status_rejected():
    resp = client.post("/tasks", json={"title": "t", "status": "Unknown"})
    assert resp.status_code == 422


# ---------------------------------------------------------------------------
# GET /tasks – list
# ---------------------------------------------------------------------------

def test_list_tasks_empty():
    resp = client.get("/tasks")
    assert resp.status_code == 200
    assert resp.json() == []


def test_list_tasks_returns_created():
    client.post("/tasks", json={"title": "Task A"})
    client.post("/tasks", json={"title": "Task B"})
    resp = client.get("/tasks")
    assert resp.status_code == 200
    titles = {t["title"] for t in resp.json()}
    assert titles == {"Task A", "Task B"}


# ---------------------------------------------------------------------------
# GET /tasks/{id} – get by id
# ---------------------------------------------------------------------------

def test_get_task_by_id():
    created = client.post("/tasks", json={"title": "Find me"}).json()
    resp = client.get(f"/tasks/{created['id']}")
    assert resp.status_code == 200
    assert resp.json()["id"] == created["id"]


def test_get_task_not_found():
    resp = client.get("/tasks/nonexistent-id")
    assert resp.status_code == 404


# ---------------------------------------------------------------------------
# DELETE /tasks/{id}
# ---------------------------------------------------------------------------

def test_delete_task():
    created = client.post("/tasks", json={"title": "Delete me"}).json()
    resp = client.delete(f"/tasks/{created['id']}")
    assert resp.status_code == 204
    assert client.get(f"/tasks/{created['id']}").status_code == 404


def test_delete_task_not_found():
    resp = client.delete("/tasks/nonexistent-id")
    assert resp.status_code == 404


# ---------------------------------------------------------------------------
# PATCH /tasks/{id} – update
# ---------------------------------------------------------------------------

def test_patch_task_title():
    created = client.post("/tasks", json={"title": "Old title"}).json()
    resp = client.patch(f"/tasks/{created['id']}", json={"title": "New title"})
    assert resp.status_code == 200
    assert resp.json()["title"] == "New title"


def test_patch_task_not_found():
    resp = client.patch("/tasks/nonexistent-id", json={"title": "x"})
    assert resp.status_code == 404


# ---------------------------------------------------------------------------
# Status transitions
# ---------------------------------------------------------------------------

def test_transition_todo_to_inprogress():
    task = client.post("/tasks", json={"title": "t"}).json()
    resp = client.patch(f"/tasks/{task['id']}", json={"status": "InProgress"})
    assert resp.status_code == 200
    assert resp.json()["status"] == "InProgress"


def test_transition_inprogress_to_done():
    task = client.post("/tasks", json={"title": "t", "status": "InProgress"}).json()
    resp = client.patch(f"/tasks/{task['id']}", json={"status": "Done"})
    assert resp.status_code == 200
    assert resp.json()["status"] == "Done"


def test_transition_done_to_inprogress():
    task = client.post("/tasks", json={"title": "t", "status": "Done"}).json()
    resp = client.patch(f"/tasks/{task['id']}", json={"status": "InProgress"})
    assert resp.status_code == 200
    assert resp.json()["status"] == "InProgress"


def test_transition_todo_to_done_rejected():
    task = client.post("/tasks", json={"title": "t"}).json()
    resp = client.patch(f"/tasks/{task['id']}", json={"status": "Done"})
    assert resp.status_code == 422


def test_transition_inprogress_to_todo_rejected():
    task = client.post("/tasks", json={"title": "t", "status": "InProgress"}).json()
    resp = client.patch(f"/tasks/{task['id']}", json={"status": "ToDo"})
    assert resp.status_code == 422


def test_transition_done_to_todo_rejected():
    task = client.post("/tasks", json={"title": "t", "status": "Done"}).json()
    resp = client.patch(f"/tasks/{task['id']}", json={"status": "ToDo"})
    assert resp.status_code == 422
