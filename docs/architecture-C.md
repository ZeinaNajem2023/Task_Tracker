# Task Tracker Architecture

## 1. What the app does

Task Tracker is a FastAPI REST API for creating, listing, retrieving, partially updating, and deleting tasks. It stores tasks in memory and exposes a health-check route. A user interface and its behavior are not visible from the files I read.

## 2. Data model

The main entity is **Task**, represented by three Pydantic models:

- `TaskCreate`: `title`, optional `description`, `status`, `priority`, and optional `assignee`
- `TaskUpdate`: optional versions of all editable fields
- `TaskResponse`: editable fields plus `id`, `created_at`, and `updated_at`

Statuses are `ToDo`, `InProgress`, and `Done`. Priorities are `Low`, `Medium`, and `High`. New tasks default to `ToDo` and `Medium`.

## 3. Request flow: creating a task

1. How the user initiates creation is not visible from the files I read.
2. A client sends task data to `POST /tasks`.
3. FastAPI parses it as `TaskCreate`; Pydantic validates field types, enum values, extra fields, and the title.
4. `app/main.py` calls `storage.add_task()`.
5. Storage generates a UUID and current UTC timestamps, builds a `TaskResponse`, and places it in the module-level `_tasks` dictionary.
6. FastAPI returns the created task with HTTP 201.

## 4. Key files

- `app/main.py` — Configures FastAPI and CORS and defines the task endpoints.
- `app/models.py` — Defines task schemas, enums, defaults, and title validation.
- `app/storage.py` — Implements in-memory task creation, retrieval, update, deletion, and internal filtering.
- `app/business_rules.py` — Supplies the imported status-transition validator; its implementation is not visible from the files I read.
- `app/routers/health.py` — Supplies the included health router; its implementation is not visible from the files I read.

## 5. Conventions

- **Validation:** Pydantic models forbid extra fields. Titles are trimmed, must not be blank, and cannot exceed 200 characters.
- **Storage:** Tasks are stored by string UUID in a module-level dictionary. Updates copy the existing model and refresh `updated_at`.
- **Error handling:** Missing tasks produce HTTP 404 responses. Invalid status transitions are documented in `main.py` as HTTP 422; their detailed rules are not visible from the files I read. Other validation-error behavior is not visible from the files I read.
- **Frontend/backend interaction:** A frontend is not visible from the files I read. CORS allows specified `localhost` and `127.0.0.1` origins on ports 5500 and 8000.

## 6. Not visible or assumptions

Frontend structure, user-interface behavior, health-response details, status-transition rules, test coverage, deployment, authentication, and database support are not visible from the files I read. The in-memory dictionary establishes process-local storage, but runtime topology and restart behavior are not visible from the files I read.
