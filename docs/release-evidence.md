# Release Evidence

## Baseline

- Branch: final-project
- Date: 2026-08-08
- Local app run command: `uvicorn app.main:app --reload --port 8000`
- GET /health returned HTTP 200 OK.
- The Kanban board loaded successfully.
- I manually exercised the New Task create flow and the Edit flow successfully.
- Test command: python -m pytest -v
- Test result: 20 passed in 0.73s

## CI evidence

- Workflow file: [.github/workflows/ci.yml](.github/workflows/ci.yml)
- CI test command: pytest -v
- continue-on-error: Not present
- `|| true`: Not present
- `--exit-zero`: Not present
- Pytest skipped: Not present
- Vague Python version: Not present (pinned to 3.11)
- Missing dependency installation: Not present (installs from requirements.txt)
- Latest run link/note: GitHub Actions workflow ran successfully on the final-project branch (CI #18, commit 2c76332).

## Docker evidence

- Docker build check: Passed. `docker build -t task-tracker .` completed successfully and created `task-tracker:latest`.
- Docker run check: Passed. `docker run --rm -d --name task-tracker-final -p 8000:8000 task-tracker` started the container successfully.
- Docker /health check: Passed. `curl.exe -i http://127.0.0.1:8000/health` returned `HTTP/1.1 200 OK` with a JSON status of `"ok"`.
- Non-root check: Passed. `docker exec task-tracker-final id` returned `uid=100(app) gid=101(app) groups=101(app)`, and `docker inspect --format '{{.Config.User}}' task-tracker-final` returned `app`.
- No-baked-secrets check: Passed. A runtime filesystem check with `find /app -maxdepth 2 -type f -print` showed only application files and `requirements.txt` under `/app`, with no `.env` file present. The repository's `.dockerignore` also excludes `.env` and `.env.*`.

## Documentation claim-vs-reality log

| Claim checked                                   | Evidence used                                                                                                                                                    | Result                                  | Change made, if any                                                                                  |
| ----------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| README local API command and `/health` behavior | Ran `uvicorn app.main:app --reload --port 8000`; GET `/health` returned HTTP 200                                                                                 | Verified after documentation correction | Corrected the escaped local run command and documented the verified health behavior                  |
| README local test command and result            | Ran `python -m pytest -v`; result was `20 passed in 0.73s`                                                                                                       | Verified                                | Documented the locally verified test command/result; CI remains separately documented as `pytest -v` |
| README Docker build/run/health/non-root claims  | `docker build` succeeded; container ran successfully; `/health` returned HTTP 200; `docker exec ... id` returned `uid=100(app)` and Docker config user was `app` | Verified                                | Updated README Docker commands to the exact workflow that was successfully tested                    |
