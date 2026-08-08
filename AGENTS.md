# Module 4 Task Tracker - AGENTS.md

## 1. Tech stack

- Python 3.11
- FastAPI
- Pydantic v2
- Uvicorn
- pytest
- httpx
- Vanilla JavaScript frontend is present (single-page UI in frontend/index.html).

## 2. Run command (course standard)

`uvicorn app.main:app --reload --port 8000`

## 3. Test command (course standard)

`pytest -v`

## 4. Architecture summary

- Backend:
  - app/main.py: FastAPI app setup, CORS middleware, and task CRUD endpoints (create, list, get by id, update, delete).
  - app/models.py: Pydantic models and validation for task create/update/response payloads, including title rules and enum-backed status/priority values.
  - app/storage.py: In-memory task store with helper support for exact-match status and priority filtering; the current GET /tasks endpoint does not expose those filters.
  - app/business_rules.py: status transition validation for the allowed task state changes.
  - app/routers/health.py: health endpoint router included by app/main.py.
- Frontend:
  - frontend/index.html: Vanilla JavaScript Kanban-style UI for viewing tasks by status, creating/editing tasks, and updating task status.
- Tests:
  - tests/test_baseline_crud.py: API-level coverage for health, CRUD, and status-transition behavior.
  - tests/verify_a.py: a standalone validation script for model-field and enum behavior; it is not collected by pytest by default.
- Where task rules live:
  - Status transition rules: app/business_rules.py.
  - Input/data validation rules: app/models.py.
  - In-memory filtering helpers: app/storage.py.

## 5. Business rules (implemented)

- Task status values:
  - ToDo
  - InProgress
  - Done
- Allowed status transitions:
  - ToDo -> InProgress
  - InProgress -> Done
  - Done -> InProgress
- Any transition not listed above is rejected with 422.
- Transition validation is applied when PATCH payload includes status.

## 6. UI states and CORS notes

- UI states present in frontend:
  - Board loading state.
  - Board error state.
  - Ready/normal board render state.
  - Empty-column state message.
  - Modal open/close state for create/edit task.
  - Drag-and-drop visual states (dragging card, drag-over column).
  - Inline form validation/error banner states.
- CORS (backend):
  - Enabled via CORSMiddleware in app/main.py.
  - Allowed origins: `http://localhost:5500`, `http://127.0.0.1:5500`, `http://localhost:8000`, `http://127.0.0.1:8000`
  - `allow_credentials`: true
  - `allow_methods`: `*`
  - `allow_headers`: `*`

## 7. Read-first and docs-first guardrails

- Read the relevant existing files before proposing code changes.
- For release-readiness, architecture, workflow, or behavior questions, check existing documentation and repository evidence before editing code.
- Do not modify app/ or frontend/ unless the task explicitly requires a small bug fix, security fix, or documented correction.
- Prefer documentation or configuration corrections when the code is already correct.
- Show proposed diffs before applying changes when practical.

## 8. Do-not rules

- Do not add authentication unless explicitly requested.
- Do not add a database/persistence layer unless explicitly requested.
- Do not add deployment/DevOps steps unless explicitly requested.
- Do not make major UI redesigns or scope-expanding UI changes without asking first.
