from datetime import date, timedelta

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app import storage


@pytest.fixture(autouse=True)
def reset_storage() -> None:
    storage._reset()
    yield
    storage._reset()


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_create_task_with_valid_due_date(client: TestClient) -> None:
    payload = {
        "title": "Write tests",
        "description": "Feature 1 coverage",
        "due_date": "2026-08-15",
    }

    response = client.post("/tasks", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == payload["title"]
    assert data["description"] == payload["description"]
    assert data["due_date"] == payload["due_date"]


def test_create_task_with_invalid_due_date_returns_422(client: TestClient) -> None:
    response = client.post(
        "/tasks",
        json={
            "title": "Bad due date",
            "due_date": "not-a-date",
        },
    )

    assert response.status_code == 422
    detail = response.json()["detail"]
    assert any(error.get("loc", [])[-1] == "due_date" for error in detail)


def test_update_and_clear_due_date(client: TestClient) -> None:
    create_response = client.post("/tasks", json={"title": "Patch me"})
    assert create_response.status_code == 201
    task = create_response.json()
    task_id = task["id"]
    assert task["due_date"] is None

    set_due_date_response = client.patch(
        f"/tasks/{task_id}",
        json={"due_date": "2026-09-01"},
    )
    assert set_due_date_response.status_code == 200
    updated = set_due_date_response.json()
    assert updated["due_date"] == "2026-09-01"
    assert updated["title"] == "Patch me"

    clear_due_date_response = client.patch(
        f"/tasks/{task_id}",
        json={"due_date": None},
    )
    assert clear_due_date_response.status_code == 200
    cleared = clear_due_date_response.json()
    assert cleared["due_date"] is None
    assert cleared["title"] == "Patch me"


def test_overdue_filter_returns_only_overdue_non_done_tasks(client: TestClient) -> None:
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    today = date.today().isoformat()
    tomorrow = (date.today() + timedelta(days=1)).isoformat()

    overdue_todo = client.post(
        "/tasks",
        json={
            "title": "Overdue ToDo",
            "status": "ToDo",
            "due_date": yesterday,
        },
    ).json()
    overdue_in_progress = client.post(
        "/tasks",
        json={
            "title": "Overdue InProgress",
            "status": "InProgress",
            "due_date": yesterday,
        },
    ).json()
    client.post(
        "/tasks",
        json={
            "title": "Due today",
            "status": "ToDo",
            "due_date": today,
        },
    )
    client.post(
        "/tasks",
        json={
            "title": "Done in past",
            "status": "Done",
            "due_date": yesterday,
        },
    )
    client.post(
        "/tasks",
        json={
            "title": "No due date",
            "status": "ToDo",
        },
    )
    client.post(
        "/tasks",
        json={
            "title": "Future due date",
            "status": "InProgress",
            "due_date": tomorrow,
        },
    )

    response = client.get("/tasks?overdue=true")

    assert response.status_code == 200
    overdue_ids = {task["id"] for task in response.json()}
    assert overdue_ids == {overdue_todo["id"], overdue_in_progress["id"]}
