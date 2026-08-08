# Task Tracker Architecture

## 1. What the app does

Task Tracker is a learning-focused task management app with a FastAPI backend and a single-page vanilla JavaScript Kanban UI. Users can create, retrieve, update, delete, filter, search, and move tasks through the `ToDo`, `InProgress`, and `Done` states.

## 2. Data model

The primary entity is **Task**, represented by separate Pydantic models for creation, partial updates, and responses.

Important fields:

- `id`: generated task identifier
- `title`: required task name
- `description`: optional details
- `status`: `ToDo`, `InProgress`, or `Done`
- `priority`: `Low`, `Medium`, or `High`
- `assignee`: optional owner
- `created_at` and `updated_at`: task timestamps
- `due_date`: due-date information described by the repository context

## 3. Request flow: creating a task

1. The user enters task details in the frontend modal.
2. Frontend JavaScript sends a `POST /tasks` request to the FastAPI backend.
3. FastAPI parses and validates the request using the `TaskCreate` Pydantic model.
4. The route delegates creation to `app/storage.py`.
5. Storage generates the task identifier and timestamps and adds the task to the in-memory store.
6. The API returns the created task with HTTP 201.
7. The frontend updates its local task list and rerenders the board.

## 4. Key files

- `app/main.py` — Configures FastAPI, CORS, routers, and task CRUD endpoints.
- `app/models.py` — Defines task models, enums, defaults, and field validation.
- `app/storage.py` — Manages in-memory CRUD, filtering, overdue checks, and search.
- `app/business_rules.py` — Defines and validates permitted status transitions.
- `app/routers/health.py` — Provides the API health endpoint.
- `frontend/index.html` — Implements the Kanban UI, modal, filters, API calls, and drag-and-drop.
- `tests/test_baseline_crud.py` — Covers CRUD operations and status transitions.
- `tests/test_feature1_due_date.py` — Covers due dates and overdue filtering.
- `tests/test_feature2_search.py` — Covers search and combined filters.

## 5. Conventions

- **Validation:** Pydantic v2 models validate input. Status and priority use enums, and unexpected fields are rejected.
- **Business rules:** Valid transitions are `ToDo → InProgress`, `InProgress → Done`, and `Done → InProgress`; other transitions return HTTP 422.
- **Storage:** Tasks are held in memory, so data is lost when the application process restarts.
- **Error handling:** Invalid input and transitions produce HTTP 422 responses; requests for missing tasks produce HTTP 404 responses.
- **Frontend/backend interaction:** The frontend uses HTTP API calls and client-side rendering. CORS permits the documented local ports on `localhost` and `127.0.0.1`.

## 6. Not visible or assumptions

Authentication, database persistence, and deployment behavior are not part of the documented architecture. The supplied file-summary item contained only the placeholder `UMMARY`, so details beyond AGENTS.md were confirmed from repository files inspected during this task’s preceding architecture review.
