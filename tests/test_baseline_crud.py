import pytest
from fastapi.testclient import TestClient

from app.main import app
from app import storage


@pytest.fixture(autouse=True)
def reset_storage():
    storage._reset()
    yield
    storage._reset()


client = TestClient(app)


# ---------------------------------------------------------------------------
# POST /tasks – create
# ---------------------------------------------------------------------------

def test_create_task_returns_201():
    response = client.post("/tasks", json={"title": "My Task"})
    assert response.status_code == 201


def test_create_task_response_fields():
    response = client.post("/tasks", json={"title": "My Task"})
    data = response.json()
    assert data["title"] == "My Task"
    assert data["status"] == "ToDo"
    assert data["priority"] == "Medium"
    assert data["description"] == ""
    assert data["assignee"] is None
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_create_task_blank_title_returns_422():
    response = client.post("/tasks", json={"title": "   "})
    assert response.status_code == 422


def test_create_task_empty_title_returns_422():
    response = client.post("/tasks", json={"title": ""})
    assert response.status_code == 422


def test_create_task_title_too_long_returns_422():
    response = client.post("/tasks", json={"title": "x" * 201})
    assert response.status_code == 422


def test_create_task_title_max_length_accepted():
    response = client.post("/tasks", json={"title": "x" * 200})
    assert response.status_code == 201


def test_create_task_extra_field_returns_422():
    response = client.post("/tasks", json={"title": "Task", "unknown_field": "value"})
    assert response.status_code == 422


def test_create_task_with_all_fields():
    response = client.post("/tasks", json={
        "title": "Full Task",
        "description": "A description",
        "status": "InProgress",
        "priority": "High",
        "assignee": "alice",
    })
    assert response.status_code == 201
    data = response.json()
    assert data["description"] == "A description"
    assert data["status"] == "InProgress"
    assert data["priority"] == "High"
    assert data["assignee"] == "alice"


# ---------------------------------------------------------------------------
# GET /tasks – list
# ---------------------------------------------------------------------------

def test_list_tasks_empty():
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_returns_created_tasks():
    client.post("/tasks", json={"title": "Task A"})
    client.post("/tasks", json={"title": "Task B"})
    response = client.get("/tasks")
    assert response.status_code == 200
    assert len(response.json()) == 2


# ---------------------------------------------------------------------------
# GET /tasks/{task_id} – get by id
# ---------------------------------------------------------------------------

def test_get_task_by_id():
    created = client.post("/tasks", json={"title": "Find Me"}).json()
    response = client.get(f"/tasks/{created['id']}")
    assert response.status_code == 200
    assert response.json()["title"] == "Find Me"


def test_get_task_not_found_returns_404():
    response = client.get("/tasks/nonexistent-id")
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# PATCH /tasks/{task_id} – update
# ---------------------------------------------------------------------------

def test_patch_task_title():
    created = client.post("/tasks", json={"title": "Old Title"}).json()
    response = client.patch(f"/tasks/{created['id']}", json={"title": "New Title"})
    assert response.status_code == 200
    assert response.json()["title"] == "New Title"


def test_patch_task_not_found_returns_404():
    response = client.patch("/tasks/nonexistent-id", json={"title": "X"})
    assert response.status_code == 404


def test_patch_task_extra_field_returns_422():
    created = client.post("/tasks", json={"title": "Task"}).json()
    response = client.patch(f"/tasks/{created['id']}", json={"made_up": "value"})
    assert response.status_code == 422


# ---------------------------------------------------------------------------
# DELETE /tasks/{task_id} – delete
# ---------------------------------------------------------------------------

def test_delete_task_returns_204():
    created = client.post("/tasks", json={"title": "Delete Me"}).json()
    response = client.delete(f"/tasks/{created['id']}")
    assert response.status_code == 204


def test_delete_task_not_found_returns_404():
    response = client.delete("/tasks/nonexistent-id")
    assert response.status_code == 404


def test_delete_task_removes_from_list():
    created = client.post("/tasks", json={"title": "Gone"}).json()
    client.delete(f"/tasks/{created['id']}")
    response = client.get("/tasks")
    assert response.json() == []


# ---------------------------------------------------------------------------
# Status transitions
# ---------------------------------------------------------------------------

def test_valid_transition_todo_to_inprogress():
    created = client.post("/tasks", json={"title": "Task"}).json()
    response = client.patch(f"/tasks/{created['id']}", json={"status": "InProgress"})
    assert response.status_code == 200
    assert response.json()["status"] == "InProgress"


def test_valid_transition_inprogress_to_done():
    created = client.post("/tasks", json={"title": "Task", "status": "InProgress"}).json()
    response = client.patch(f"/tasks/{created['id']}", json={"status": "Done"})
    assert response.status_code == 200
    assert response.json()["status"] == "Done"


def test_valid_transition_done_to_inprogress():
    created = client.post("/tasks", json={"title": "Task", "status": "Done"}).json()
    response = client.patch(f"/tasks/{created['id']}", json={"status": "InProgress"})
    assert response.status_code == 200
    assert response.json()["status"] == "InProgress"


def test_invalid_transition_todo_to_done_returns_422():
    created = client.post("/tasks", json={"title": "Task"}).json()
    response = client.patch(f"/tasks/{created['id']}", json={"status": "Done"})
    assert response.status_code == 422


def test_invalid_transition_inprogress_to_todo_returns_422():
    created = client.post("/tasks", json={"title": "Task", "status": "InProgress"}).json()
    response = client.patch(f"/tasks/{created['id']}", json={"status": "ToDo"})
    assert response.status_code == 422


def test_invalid_transition_done_to_todo_returns_422():
    created = client.post("/tasks", json={"title": "Task", "status": "Done"}).json()
    response = client.patch(f"/tasks/{created['id']}", json={"status": "ToDo"})
    assert response.status_code == 422
