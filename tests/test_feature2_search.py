import pytest
from fastapi.testclient import TestClient

from app import storage
from app.main import app


@pytest.fixture(autouse=True)
def reset_storage() -> None:
    storage._reset()
    yield
    storage._reset()


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_search_by_title(client: TestClient) -> None:
    matching = client.post(
        "/tasks",
        json={"title": "Release roadmap", "description": "Milestone planning"},
    ).json()
    client.post(
        "/tasks",
        json={"title": "Write docs", "description": "Documentation task"},
    )

    response = client.get("/tasks?search=road")

    assert response.status_code == 200
    result_ids = {task["id"] for task in response.json()}
    assert result_ids == {matching["id"]}


def test_search_by_description(client: TestClient) -> None:
    matching = client.post(
        "/tasks",
        json={"title": "Backend cleanup", "description": "Refactor legacy parser"},
    ).json()
    client.post(
        "/tasks",
        json={"title": "Frontend polish", "description": "Improve spacing"},
    )

    response = client.get("/tasks?search=legacy")

    assert response.status_code == 200
    result_ids = {task["id"] for task in response.json()}
    assert result_ids == {matching["id"]}


def test_case_insensitive_search(client: TestClient) -> None:
    matching = client.post(
        "/tasks",
        json={"title": "BUG triage", "description": "Weekly review"},
    ).json()
    client.post(
        "/tasks",
        json={"title": "Planning", "description": "Prepare backlog"},
    )

    response = client.get("/tasks?search=bug")

    assert response.status_code == 200
    result_ids = {task["id"] for task in response.json()}
    assert result_ids == {matching["id"]}


def test_combined_status_priority_and_search_filters(client: TestClient) -> None:
    matching = client.post(
        "/tasks",
        json={
            "title": "API integration",
            "description": "Connect service",
            "status": "InProgress",
            "priority": "High",
        },
    ).json()
    client.post(
        "/tasks",
        json={
            "title": "API notes",
            "description": "Wrong status",
            "status": "ToDo",
            "priority": "High",
        },
    )
    client.post(
        "/tasks",
        json={
            "title": "API migration",
            "description": "Wrong priority",
            "status": "InProgress",
            "priority": "Low",
        },
    )
    client.post(
        "/tasks",
        json={
            "title": "Release prep",
            "description": "No search match",
            "status": "InProgress",
            "priority": "High",
        },
    )

    response = client.get("/tasks?status=InProgress&priority=High&search=api")

    assert response.status_code == 200
    result_ids = {task["id"] for task in response.json()}
    assert result_ids == {matching["id"]}


def test_no_search_matches_returns_empty_list_with_200(client: TestClient) -> None:
    client.post(
        "/tasks",
        json={"title": "Write tests", "description": "Coverage for feature 2"},
    )
    client.post(
        "/tasks",
        json={"title": "Update docs", "description": "ADR revisions"},
    )

    response = client.get("/tasks?search=notfound")

    assert response.status_code == 200
    assert response.json() == []
