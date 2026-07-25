import pytest
from fastapi.testclient import TestClient

from app import storage
from app.main import app


@pytest.fixture(autouse=True)
def reset_storage():
    storage._reset()
    yield
    storage._reset()


@pytest.fixture
def client():
    return TestClient(app)


def test_create_and_get_task(client):
    response = client.post("/tasks", json={"title": "Baseline task"})
    assert response.status_code == 201

    task = response.json()

    response = client.get(f"/tasks/{task['id']}")
    assert response.status_code == 200
    assert response.json()["title"] == "Baseline task"


def test_update_task(client):
    task = client.post("/tasks", json={"title": "Original"}).json()

    response = client.patch(
        f"/tasks/{task['id']}",
        json={"title": "Updated"},
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Updated"


def test_list_tasks_returns_created_items(client):
    task_a = client.post("/tasks", json={"title": "Task A"}).json()
    task_b = client.post("/tasks", json={"title": "Task B"}).json()

    response = client.get("/tasks")

    assert response.status_code == 200
    ids = {task["id"] for task in response.json()}
    assert ids == {task_a["id"], task_b["id"]}


def test_delete_task_removes_task(client):
    task = client.post("/tasks", json={"title": "Delete me"}).json()

    delete_response = client.delete(f"/tasks/{task['id']}")
    get_response = client.get(f"/tasks/{task['id']}")

    assert delete_response.status_code == 204
    assert get_response.status_code == 404


def test_get_update_delete_missing_task_return_404(client):
    missing_id = "missing-task-id"

    get_response = client.get(f"/tasks/{missing_id}")
    patch_response = client.patch(
        f"/tasks/{missing_id}",
        json={"title": "Nope"},
    )
    delete_response = client.delete(f"/tasks/{missing_id}")

    assert get_response.status_code == 404
    assert patch_response.status_code == 404
    assert delete_response.status_code == 404


def test_valid_status_transitions_are_allowed(client):
    task = client.post(
        "/tasks",
        json={"title": "Transition task", "status": "ToDo"},
    ).json()

    to_in_progress = client.patch(
        f"/tasks/{task['id']}",
        json={"status": "InProgress"},
    )

    to_done = client.patch(
        f"/tasks/{task['id']}",
        json={"status": "Done"},
    )

    back_to_in_progress = client.patch(
        f"/tasks/{task['id']}",
        json={"status": "InProgress"},
    )

    assert to_in_progress.status_code == 200
    assert to_in_progress.json()["status"] == "InProgress"

    assert to_done.status_code == 200
    assert to_done.json()["status"] == "Done"

    assert back_to_in_progress.status_code == 200
    assert back_to_in_progress.json()["status"] == "InProgress"


def test_invalid_status_transitions_return_422(client):
    todo_task = client.post(
        "/tasks",
        json={"title": "Todo task", "status": "ToDo"},
    ).json()

    done_task = client.post(
        "/tasks",
        json={"title": "Done task", "status": "Done"},
    ).json()

    todo_to_done = client.patch(
        f"/tasks/{todo_task['id']}",
        json={"status": "Done"},
    )

    done_to_todo = client.patch(
        f"/tasks/{done_task['id']}",
        json={"status": "ToDo"},
    )

    assert todo_to_done.status_code == 422
    assert "Invalid status transition" in todo_to_done.json()["detail"]

    assert done_to_todo.status_code == 422
    assert "Invalid status transition" in done_to_todo.json()["detail"]