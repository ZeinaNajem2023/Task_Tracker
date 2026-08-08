# Final AI Review and Ownership Evidence

## AGENTS.md guardrails

- Repo-specific stack and commands included: yes
- Docs-first/read-first guardrail included: yes
- Unexpected app/frontend edits rule included: yes

AGENTS.md tells an AI assistant to read the relevant existing files and repository evidence first, and to prefer documentation or configuration changes over app or frontend edits unless the task clearly requires a small fix.

## AI code review mini-log

Reviewing .github/workflows/ci.yml.

| AI comment                                                                                                                                                                                                               | Grade: Useful / Noise / Wrong | Reason                                                                                                                                                                 | Verification or decision                                       |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| The workflow installs dependencies directly from requirements.txt on every run and does not show dependency caching or a lock file, so CI can spend time reinstalling the same packages on each push or pull request.    | Noise                         | requirements.txt is version-pinned and caching is an optional performance improvement, not required for correctness or this project scope.                             | No CI change; keep the workflow simple.                        |
| The workflow uses a single Python 3.11 environment and does not pin the execution environment beyond the version string, which makes the job less reproducible if the runtime or dependency set changes.                 | Useful                        | ubuntu-latest can change over time, so the reproducibility observation is technically reasonable, but Python is explicitly pinned to 3.11 and CI is currently passing. | Acknowledge the tradeoff; no change required for this release. |
| The workflow runs pytest directly after installation but does not include any explicit dependency integrity or audit step, so it does not provide extra evidence about package consistency or known supply-chain issues. | Noise                         | package-audit tooling is outside the required CI scope.                                                                                                                | Reject as scope expansion.                                     |

## AI security mini-review

| Finding                                                                                                         | File evidence                                                                                                | Grade: Valid / False Positive / Noise | Reason                                                                                                                                                                | Next action                    |
| --------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ | ------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------ |
| The earlier "unauthenticated CRUD" concern is not a release issue for this repository's learning-project scope. | app/main.py defines the task CRUD routes, and AGENTS.md explicitly excludes authentication unless requested. | False Positive                        | authentication is explicitly excluded from this learning-project scope.                                                                                               | None for this release.         |
| The local CORS configuration does not show an actionable release issue.                                         | app/main.py enables CORSMiddleware for localhost/127.0.0.1 origins only.                                     | Noise                                 | origins are restricted to localhost/127.0.0.1 development addresses; no actionable release issue was demonstrated.                                                    | None for this release.         |
| The earlier "unbounded strings/in-memory capacity" finding was rejected as written.                             | app/models.py validates title length, and app/storage.py is an in-memory task store.                         | Noise                                 | The finding is partly inaccurate because title length is validated, and the remaining in-memory capacity concern is not actionable for this learning-project release. | Reject the finding as written. |

## Manual security check

I manually reviewed tracked files for .env files and searched the repository for terms including API key, secret, password, token, and credential. The only tracked environment file was .env.example, which contains only PORT=8000 and APP_ENV=development. The keyword matches were configuration names or documentation references rather than real credentials. I found no real secrets, tokens, passwords, or customer/personal data in the checked repository content.

## One AI output I rejected or corrected

An earlier AI-assisted version of AGENTS.md described due-date, overdue, and search features and referenced test files that did not exist in the repository. I rejected those claims after a read-only repository check showed that they were inaccurate. I updated AGENTS.md to describe only the actual baseline CRUD/status-transition behavior and the real test files, and clarified that storage.py contains status/priority filtering helpers that the current GET /tasks endpoint does not expose.

## Three AI usage rules

1. Never paste: passwords, API keys, secrets, credentials, or real personal/customer data.
2. Always verify: AI-generated changes against the actual repository, diffs, commands, and test results.
3. Record AI contributions by: documenting important AI suggestions, my judgment of them, and any corrections or rejections I made.

## Ownership statement

I am comfortable submitting this repository as my work because I reviewed the AI-assisted changes instead of accepting them automatically. I verified the application manually, ran the test suite, checked the CI workflow, and corrected documentation when AI claims did not match the repository. I can explain the project structure, commands, business rules, and the release evidence included in this submission. AI supported the work, but I made the final decisions about what to keep, correct, or reject.
