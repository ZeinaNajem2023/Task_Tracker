# Release Evidence

## Baseline

- Branch: final-project
- Date: 2026-08-09
- Local app run command: `uvicorn app.main:app --reload --port 8000`
- /health command: `Invoke-RestMethod http://127.0.0.1:8000/health | ConvertTo-Json -Compress`
- /health result: `{"status":"ok","timestamp":"2026-08-09T11:09:59.273443+00:00"}`
- Frontend check: opened `frontend/index.html` while the backend was running; the Kanban board rendered, the New Task modal opened, and the Edit Task modal opened for a seeded task.
- Test command: `python -m pytest -v`
- Test result: 20 passed

## CI evidence

- Workflow file: [.github/workflows/ci.yml](.github/workflows/ci.yml)
- Latest run link/note: CI run #24 completed successfully on `final-project`: https://github.com/ZeinaNajem2023/Task_Tracker/actions/runs/31309896192
- CI test command: `python -m pytest -v`
- continue-on-error: Not present
- `|| true`: Not present
- `--exit-zero`: Not present
- Pytest skipped: Not present
- Vague Python version: Not present (pinned to 3.11)
- Missing dependency installation: Not present (installs from requirements.txt)

## Docker evidence

- Build command: `docker build -t task-tracker-final-check .`
- Run command: `docker run --rm -d --name task-tracker-final-check -p 8001:8000 task-tracker-final-check`
- /health check: `curl.exe -i http://127.0.0.1:8001/health` returned `HTTP/1.1 200 OK` and `{"status":"ok",...}`.
- Non-root check: `docker exec task-tracker-final-check sh -lc "id"` returned `uid=100(app) gid=101(app) groups=101(app)`, and `docker inspect --format '{{.Config.User}}' task-tracker-final-check` returned `app`.
- No-baked-secrets check: `docker exec task-tracker-final-check sh -lc "find /app -maxdepth 2 -type f | sort"` listed only the application Python files plus `requirements.txt`; no `.env` file was present. `.dockerignore` excludes `.env` and `.env.*`.

## Documentation claim-vs-reality log

| Claim checked                                   | Evidence used                                                                                                                                                                                                              | Result   | Change made, if any                                                          |
| ----------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- | ---------------------------------------------------------------------------- |
| README local API command and `/health` behavior | Ran `uvicorn app.main:app --reload --port 8000`; then ran `Invoke-RestMethod http://127.0.0.1:8000/health` and confirmed the expected JSON payload.                                                                        | Verified | Kept the documented command and added the exact verification command/result. |
| README local test command and result            | Ran `python -m pytest -v`; result was `20 passed`.                                                                                                                                                                         | Verified | Kept the command and recorded the verified result.                           |
| README Docker build/run/health/non-root claims  | Ran `docker build -t task-tracker-final-check .`; `docker run --rm -d --name task-tracker-final-check -p 8001:8000 ...`; `curl.exe -i http://127.0.0.1:8001/health`; and `docker inspect --format '{{.Config.User}}' ...`. | Verified | Updated the README Docker section to match the validated workflow.           |
| README frontend baseline claim                  | Opened `frontend/index.html`; observed the board render, New Task modal, and Edit Task modal for a seeded task.                                                                                                            | Verified | Clarified the Final Project summary so it reflects the checked UI behavior.  |
