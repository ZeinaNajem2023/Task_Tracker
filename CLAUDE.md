# Module 4 Task Tracker - CLAUDE.md

## 1. Tech stack

- Python 3.11
- FastAPI
- Pydantic v2
- Uvicorn
- pytest
- httpx
- Vanilla JavaScript frontend is present (single-page UI in frontend/index.html).

## 2. Run command (course standard)

uvicorn app.main:app --reload --port 8000

## 3. Test command (course standard)

pytest -v

## 4. Architecture summary

- Backend:
  - app/main.py: FastAPI app setup, CORS middleware, and task endpoints (POST/GET list/GET by id/PATCH/DELETE).
  - app/models.py: Pydantic models, enums, and field validation.
  - app/storage.py: In-memory task store and filtering logic (status, priority, overdue, search).
  - app/business_rules.py: status transition validation.
  - app/routers/health.py: health endpoint router, included by app/main.py.
- Frontend:
  - frontend/index.html: HTML/CSS/vanilla JS Kanban UI, modal form, drag/drop status updates, filters, and API calls.
- Tests:
  - tests/test_baseline_crud.py: CRUD and status-transition coverage.
  - tests/test_feature1_due_date.py: due date and overdue filter behavior.
  - tests/test_feature2_search.py: search and combined filter behavior.
- Where task rules live:
  - Status transition rules: app/business_rules.py.
  - Input/data validation rules: app/models.py.
  - Overdue and search filtering behavior: app/storage.py.

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
  - Allowed origins:
    - http://localhost:5500
    - http://127.0.0.1:5500
    - http://localhost:8000
    - http://127.0.0.1:8000
  - allow_credentials: true
  - allow_methods: \*
  - allow_headers: \*

## 7. Do-not rules

- Do not add authentication unless explicitly requested.
- Do not add a database/persistence layer unless explicitly requested.
- Do not add deployment/DevOps steps unless explicitly requested.
- Do not make major UI redesigns or scope-expanding UI changes without asking first.
