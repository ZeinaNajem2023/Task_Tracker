# AI Prompt Log

AI Tool Used: GitHub Copilot

## Feature 1 — Due Dates + Overdue Filter

### Prompt 1 — Models

**Prompt:** Add optional `due_date` to `TaskCreate`, `TaskUpdate`, and `TaskResponse` using Python `date`. Keep existing validation unchanged.

**Copilot Result:** Added the field to the three models.

**My Review:** Accepted after testing valid and invalid dates.

### Prompt 2 — Overdue Logic

**Prompt:** Preserve `due_date` in storage and add overdue filtering where `due_date < today` and status is not `Done`.

**Copilot Result:** Added storage support and overdue filtering.

**My Review:** Accepted after verifying the rule and running tests.

### Prompt 3 — Frontend

**Prompt:** Add due date to the modal and Kanban cards while preserving existing behaviour.

**Copilot Result:** Added date input, card display, and overdue styling.

**My Review:** Accepted after manual browser testing.

## Feature 2 — Search + Combined Filters

### Prompt 1 — Backend Search

**Prompt:** Add case-insensitive title/description search to `GET /tasks` and combine it with existing filters using AND logic.

**Copilot Result:** Added the `search` parameter and storage filtering.

**My Review:** Accepted after testing search and combined filters.

### Prompt 2 — Tests

**Prompt:** Add pytest tests for title search, description search, case-insensitive search, combined filters, and no matches.

**Copilot Result:** Created five focused tests.

**My Review:** Accepted after all tests passed.

### Prompt 3 — Frontend Filters

**Prompt:** Add search, status, and priority controls above the Kanban board using the existing API.

**Copilot Result:** Added the filter bar and query-string handling.

**My Review:** Accepted after browser verification.

## Weak Prompt Improved

**Weak:**  
`Add search to my task tracker.`

**Improved:**  
`Add an optional search parameter to GET /tasks. Search title and description case-insensitively, trim whitespace, combine with existing filters using AND logic, and preserve existing behaviour.`

**Why better:**  
The stronger prompt clearly defines the task, constraints, and expected behaviour.
