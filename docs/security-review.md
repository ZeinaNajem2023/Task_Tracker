# Security Review


## All findings

| ID | Severity | File / location | Finding | Evidence | Suggested next step | Confidence |
|---|---|---|---|---|---|---|
| SEC-01 | Medium if externally exposed; accepted for course scope | `app/main.py:35`, `AGENTS.md:74` | All task data and mutations are unauthenticated and unscoped. | The CRUD routes have no authentication or authorization dependencies. `AGENTS.md` explicitly excludes authentication unless requested. | Keep the service local/demo-only. Add authentication and per-task authorization before any shared or public deployment. | High |
| SEC-02 | Medium | `app/models.py:20`, `app/storage.py:7`, `app/main.py:54` | User-controlled data and collection growth are insufficiently bounded. | `description` and `assignee` have no length constraints, the in-memory task dictionary has no capacity control, and `GET /tasks` returns the entire collection. | Add maximum string lengths. For non-course deployment, add request/rate limits and pagination or a task-count policy. | High |
| SEC-03 | Low | `app/main.py:73`, `app/main.py:91` | Task IDs are accepted as arbitrary strings and echoed in 404 responses. | `task_id` is typed as `str` without UUID or length validation, then included in error details. | Validate IDs as UUIDs or bounded strings and consider returning a fixed `Task not found` message. | Medium |
| SEC-04 | Low | `app/main.py:24` | CORS permits credentials plus every method and header. | The origin allowlist is local, but credentials, all methods, and all headers are enabled even though the app has no credential-based authentication. | Disable credentialed CORS until needed and restrict methods and headers to those used by the application. | High |
| SEC-05 | Low | `frontend/index.html:627`, `app/main.py:26` | The frontend assumes a fixed plaintext API at `http://localhost:8000`. | The hard-coded URL does not support alternate hosts or ports and can cause mixed-content failures when the frontend uses HTTPS. | Prefer a same-origin relative path or an environment-specific validated API base URL. Use HTTPS outside local development. | High |
| SEC-06 | Low | `requirements.txt:1`, `.github/workflows/ci.yml:20` | Dependency integrity and vulnerability checks are absent. | Versions are pinned, but there are no dependency hashes, lock artifact, vulnerability audit, or automated update configuration. CI dynamically upgrades `pip`. | Add hash-locked dependencies and an appropriate dependency audit/update workflow when required by project scope. | High |
| SEC-07 | Low | `Dockerfile:1`, `.github/workflows/ci.yml:12` | Build inputs are mutable. | Docker uses the floating `python:3.11-slim` tag and GitHub Actions use moving major-version tags rather than immutable digests or commit SHAs. | Pin production base images by digest and Actions by reviewed commit SHA, with a deliberate update process. | High |

## Review limits

- This was a static review; tests, containers, and vulnerability scanners were not run.
- No external advisory database was queried, so no dependency CVEs are asserted.
- Runtime proxy, TLS, firewall, logging, and hosting configuration were not visible.
- The repository guidance identifies the project as Module 4 and contains no separate Module 5 guardrails.
