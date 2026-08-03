# Module 4 Task Tracker

## 1. Project overview

Task Tracker is a learning-project API built with FastAPI for managing tasks in memory.

Current API capabilities include:

- Health check endpoint: GET /health
- Task CRUD endpoints:
  - POST /tasks
  - GET /tasks
  - GET /tasks/{task_id}
  - PATCH /tasks/{task_id}
  - DELETE /tasks/{task_id}

The project also includes a vanilla JavaScript frontend in frontend/index.html that interacts with the API.

This module intentionally focuses on core API behavior and test coverage. It does not add authentication, database persistence, or deployment setup.

## 2. Prerequisites

- Python 3.11
- pip
- Docker Desktop (for Docker workflow)

Python packages are defined in requirements.txt:

- fastapi==0.115.6
- uvicorn[standard]==0.34.0
- pydantic==2.10.4
- python-dotenv==1.0.1
- httpx==0.28.1
- pytest==8.4.2

## 3. Local setup

Run these commands from the repository root.

Windows PowerShell:

python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt

macOS/Linux:

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt

## 4. Run the app locally

Course standard command:

uvicorn app.main:app --reload --port 8000

API base URL after startup:

- http://127.0.0.1:8000

Quick check:

curl http://127.0.0.1:8000/health

PowerShell alternative:

Invoke-RestMethod http://127.0.0.1:8000/health

## 5. Run tests

Course standard command:

pytest -v

## 6. Run with Docker

The repository includes a multi-stage Dockerfile using python:3.11-slim and a non-root runtime user named app.

Build image from repository root:

docker build -t task-tracker:dev .

Run container:

docker rm -f tt-dev 2>$null
docker run -d --name tt-dev -p 8000:8000 task-tracker:dev

Verify health endpoint through host port mapping:

curl http://127.0.0.1:8000/health

PowerShell alternative:

Invoke-RestMethod http://127.0.0.1:8000/health

Verify container runs as non-root user:

docker exec tt-dev id -un
docker exec tt-dev id -u

Stop and remove container:

docker rm -f tt-dev

## 7. CI workflow summary

GitHub Actions workflow: [.github/workflows/ci.yml](.github/workflows/ci.yml)

Current CI job:

- Triggers on push and pull_request
- Runs on ubuntu-latest
- Uses Python 3.11
- Installs dependencies from requirements.txt
- Runs tests with:
  - python -m pytest -v

## 8. Project structure

Current top-level structure:

.
├── app/
│ ├── main.py
│ ├── business_rules.py
│ ├── models.py
│ ├── storage.py
│ └── routers/
│ └── health.py
├── frontend/
│ ├── index.html
│ └── index.html.bak
├── tests/
│ ├── test_baseline_crud.py
│ └── verify_a.py
├── .github/
│ └── workflows/
│ └── ci.yml
├── Dockerfile
├── .dockerignore
├── requirements.txt
├── CLAUDE.md
└── README.md

## 9. Project conventions and current limitations

Conventions:

- Keep business rule validation in app/business_rules.py.
- Keep data validation in app/models.py.
- Keep task storage logic in app/storage.py.
- Keep route wiring and API composition in app/main.py.

Current limitations:

- In-memory storage only; data resets on process restart.
- No authentication or authorization.
- No database integration.
- No deployment or production hardening documented.
- CORS is configured for local development origins only.
- Frontend and backend are separate local components; frontend serving approach is [VERIFY].

## 10. Technical notes / decisions

Current technical note:

- [CLAUDE.md](CLAUDE.md)

[VERIFY] If you prefer a dedicated decisions path (for example docs/decisions.md), add it and update this section to point there.
