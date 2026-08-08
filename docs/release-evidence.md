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

- Docker build check: Not yet verified
- Docker run check: Not yet verified
- Docker /health check: Not yet verified
- Non-root check: Not yet verified
- No-baked-secrets check: Not yet verified

## Documentation claim-vs-reality log

| Claim checked | Evidence used | Result | Change made, if any |
| ------------- | ------------- | ------ | ------------------- |
|               |               |        |                     |
|               |               |        |                     |
|               |               |        |                     |
