"""
Task Tracker API - Application Entry Point

Creates the FastAPI application instance and registers routers.
This module is intentionally minimal for Module 1: it only wires up
the app and the health check endpoint. Future modules will register
additional routers (e.g. tasks) here.
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from app import storage
from app.business_rules import validate_status_transition
from app.models import TaskCreate, TaskResponse, TaskUpdate
from app.routers import health

app = FastAPI(
    title="Task Tracker API",
    description="A minimal learning-project REST API for tracking tasks.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500", "http://127.0.0.1:5500", "http://localhost:8000", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)


@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED, tags=["tasks"])
def create_task(payload: TaskCreate) -> TaskResponse:
    """Create a new task.

    Args:
        payload: Request body used to create the task.

    Returns:
        TaskResponse: The created task resource.

    Raises:
        None.

    Examples:
        POST /tasks
    """
    return storage.add_task(payload)


@app.get("/tasks", response_model=list[TaskResponse], tags=["tasks"])
def list_tasks() -> list[TaskResponse]:
    """List all tasks currently stored in memory.

    Args:
        None.

    Returns:
        list[TaskResponse]: All tasks in storage.

    Raises:
        None.

    Examples:
        GET /tasks
    """
    return storage.get_all_tasks()


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["tasks"])
def delete_task(task_id: str) -> None:
    """Delete a task by ID.

    Args:
        task_id: Identifier of the task to delete.

    Returns:
        None: Returns no content when deletion succeeds.

    Raises:
        HTTPException: 404 if the task ID does not exist.

    Examples:
        DELETE /tasks/{task_id}
    """
    if storage.delete_task(task_id):
        return
    raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")


@app.get("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
def get_task(task_id: str) -> TaskResponse:
    """Fetch one task by ID.

    Args:
        task_id: Identifier of the task to retrieve.

    Returns:
        TaskResponse: The matching task.

    Raises:
        HTTPException: 404 if the task ID does not exist.

    Examples:
        GET /tasks/{task_id}
    """
    task = storage.get_task_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
    return task


@app.patch("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
def update_task(task_id: str, payload: TaskUpdate) -> TaskResponse:
    """Update fields of an existing task.

    If `payload.status` is provided, status transition rules are validated
    before applying the update.

    Args:
        task_id: Identifier of the task to update.
        payload: Partial task fields to update.

    Returns:
        TaskResponse: The updated task, or the existing task if no fields are set.

    Raises:
        HTTPException: 404 if the task ID does not exist.
        HTTPException: 422 when the status transition is invalid.

    Examples:
        PATCH /tasks/{task_id}
    """
    if payload.status is not None:
        existing_task = storage.get_task_by_id(task_id)
        if existing_task is None:
            raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
        validate_status_transition(existing_task.status, payload.status)

    updated_task = storage.update_task(task_id, payload)
    if updated_task is None:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
    return updated_task