# Mini ADR: Task Filtering & Search Features

## Context

The Task Tracker application currently supports task management with status and priority filtering. User stories call for the ability to:
1. Track task due dates and identify overdue tasks
2. Search tasks by title and description
3. Combine multiple filters (status, priority, overdue, search) in a unified interface

The existing architecture uses in-memory storage, a FastAPI backend, and a Kanban board frontend. No database, authentication, or external frameworks are available.

## Decision

### Feature 1: Due Dates + Overdue Filter

- Add optional `due_date` field (date type, not datetime) to task model.
- Compute overdue status dynamically on each request: a task is overdue only if `due_date < today` and status is not `Done`; do not store an `is_overdue` flag.
- Extend GET `/tasks` endpoint to accept optional `overdue=true` query parameter for filtering.
- Update task modal form to include a date picker for due dates.
- Display due date on Kanban cards with visual indicator for overdue tasks.
- Maintain existing in-memory storage; no schema migration needed.

### Feature 2: Search + Combined Filters

- Extend GET `/tasks` endpoint with optional `search` query parameter for free-text search.
- Search matches case-insensitive substring in both title and description fields.
- Combine filters using AND logic: `status` AND `priority` AND `overdue` AND `search`.
- Add compact search/filter control bar above the Kanban board.
- Do not create a separate `/tasks/search` endpoint; reuse GET `/tasks`.

## Alternatives Considered and Rejected

| Alternative | Reason for Rejection |
|-------------|----------------------|
| **datetime + timezone handling** | Adds complexity; due dates do not require time-of-day or timezone awareness. |
| **Store `is_overdue` flag in task** | Introduces stale data; requires background updates or request-time recalculation anyway. |
| **Background job to mark overdue tasks** | Unnecessary complexity for a simple prototype; dynamic computation suffices. |
| **Frontend-only overdue filtering** | Does not reflect true overdue state; server must compute to enable API consistency. |
| **Separate `/tasks/search` endpoint** | Duplicates filter logic; single parameterized endpoint is simpler and more maintainable. |
| **Fuzzy/full-text/regex search** | Over-engineered for a small task list; substring matching is intuitive and sufficient. |
| **External search library (e.g., Whoosh, elasticsearch)** | Adds dependency and operational burden; in-memory search is adequate for prototype. |
| **Debounced client-side search requests** | Premature optimization; server and network are not bottlenecks at current scale. |

## Consequences

**Benefits:**
- Users can organize tasks by due date and identify overdue work at a glance.
- Unified search + filter interface reduces cognitive load and improves discoverability.
- Dynamic overdue computation avoids data consistency issues.
- Single parameterized endpoint eliminates API duplication.

**Trade-offs:**
- Search is limited to substring matching (no typo tolerance or ranking).
- No persistent search history or saved filters.
- Filter performance remains linear scan; acceptable only for small task lists.
- Adding indexes or a database is deferred to a future phase if scale demands it.

**Implementation Scope:**
- Backend: Update `TaskCreate`, `TaskUpdate`, and `TaskResponse`, then extend GET `/tasks` filtering logic.
- Frontend: Add date picker to modal, display due dates on cards, add search/filter bar with visual feedback.
- No schema migration or deployment complexity.
