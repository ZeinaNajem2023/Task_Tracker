# Task Tracker Architecture

## 1. What the app does

Task Tracker is a small learning-oriented task management application. A vanilla JavaScript Kanban board lets users create, view, edit, and move tasks among `ToDo`, `InProgress`, and `Done` columns, while a FastAPI backend exposes CRUD endpoints and enforces validation and status-transition rules.

## 2. Data model

The sole entity is **Task**:

- `id`: generated UUID string
- `title`: required, trimmed, nonblank, maximum 200 characters
- `description`: optional input, stored as a string; defaults to `""`
- `status`: `ToDo`, `InProgress`, or `Done`; defaults to `ToDo`
- `priority`: `Low`, `Medium`, or `High`; defaults to `Medium`
- `assignee`: optional string
- `created_at`, `updated_at`: UTC timestamps

Separate Pydantic models represent creation input, partial-update input, and API responses.

## 3. Request flow: creating a task

1. The user completes the frontend modal and selects **Create Task**.
2. Frontend validation checks required form values, then JavaScript sends JSON to `POST http://localhost:8000/tasks`.
3. FastAPI parses the body as `TaskCreate`; Pydantic rejects unknown fields and invalid titles, statuses, or priorities with HTTP 422.
4. The route calls `storage.add_task()`.
5. Storage generates a UUID and UTC timestamps, constructs a `TaskResponse`, and inserts it into the process-local `_tasks` dictionary.
6. The API returns the task with HTTP 201. The frontend adds it to local state, rerenders the board, and closes the modal.

## 4. Key files

- `app/main.py` — Creates the FastAPI app, configures CORS, and defines task CRUD routes.
- `app/models.py` — Defines task schemas, status/priority enums, defaults, and title validation.
- `app/storage.py` — Implements the in-memory task dictionary and CRUD operations.
- `app/business_rules.py` — Enforces permitted status transitions.
- `app/routers/health.py` — Provides `GET /health` with status and a UTC timestamp.
- `frontend/index.html` — Contains the entire Kanban UI, styling, form logic, drag-and-drop, and API client.
- `tests/test_baseline_crud.py` — Tests health, CRUD, validation, and status transitions.
- `requirements.txt` — Pins the Python web and testing dependencies.

## 5. Conventions

- **Validation:** Pydantic v2 validates request bodies and forbids extra fields. Titles are trimmed, required to be nonblank, and limited to 200 characters.
- **Business rules:** Status changes permit only `ToDo → InProgress`, `InProgress → Done`, and `Done → InProgress`.
- **Storage:** Tasks live in a module-level dictionary keyed by UUID; there is no database or persistence across process restarts.
- **Errors:** FastAPI/Pydantic produces HTTP 422 validation responses. Routes explicitly return HTTP 404 for missing tasks, while invalid transitions also return 422.
- **Frontend/backend interaction:** The frontend uses `fetch` against a fixed `http://localhost:8000` base URL. CORS permits designated localhost and loopback origins. After successful mutations, client-side state is updated and the board is rerendered.

## 6. Not visible or assumptions

The repository does not confirm a production deployment model, authentication, authorization, database, concurrency strategy, or how the frontend should be served. The in-memory store appears intended for local learning and testing rather than multi-process or durable production use.
