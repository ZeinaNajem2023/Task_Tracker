# Mid-Course Project User Stories

## Feature 1: Due Dates + Overdue Filter

### User Story 1 — Create a Task with a Due Date

As a user, I want to create a task with or without a due date, so that I can track deadlines only when they matter.

**Acceptance Criteria:**
1. `due_date` is optional when creating a task.
2. A task can be created successfully without a `due_date`.
3. A valid `due_date` is saved with the task.
4. An invalid date format is rejected with a clear validation error.
5. Adding `due_date` does not change the existing required task fields.

### User Story 2 — Update a Due Date

As a user, I want to add, change, or clear a task's due date, so that its deadline stays accurate when plans change.

**Acceptance Criteria:**
1. A task without a due date can be updated with a valid `due_date`.
2. An existing due date can be changed.
3. An existing due date can be cleared.
4. An invalid date format is rejected with a clear validation error.
5. Updating only `due_date` does not modify unrelated task fields.

### User Story 3 — Display Due Dates

As a user, I want to see a task's due date on its Kanban card, so that I can quickly understand upcoming deadlines.

**Acceptance Criteria:**
1. A task with a due date displays it on its Kanban card.
2. A task without a due date consistently displays "No due date" or no due-date value.
3. The displayed due date matches the value returned by the backend.
4. The correct due date remains visible after the page is refreshed.

### User Story 4 — Identify Overdue Tasks

As a user, I want overdue tasks to be clearly identifiable, so that I can prioritize work that has missed its deadline.

**Acceptance Criteria:**
1. A task is overdue only when its `due_date` is earlier than today and its status is not `Done`.
2. Tasks without a `due_date` are never considered overdue.
3. Tasks with status `Done` are never considered overdue.
4. Tasks due today are not considered overdue.
5. The existing status values remain `ToDo`, `InProgress`, and `Done`.

### User Story 5 — Filter Overdue Tasks

As a user, I want to filter the Kanban board to show overdue tasks, so that I can focus on urgent missed work.

**Acceptance Criteria:**
1. The Kanban board provides an Overdue filter.
2. Enabling the filter shows only tasks that meet the overdue rule.
3. Overdue `ToDo` and `InProgress` tasks can appear in the filtered results.
4. Tasks without due dates and tasks with status `Done` are excluded.
5. Disabling the filter restores the normal Kanban board.

### AI Assumption Corrected

Copilot initially described the overdue rule conditionally, stating that completed tasks should be excluded "if completion status exists."

I corrected this because the existing Task Tracker already has the exact statuses `ToDo`, `InProgress`, and `Done`.

**Final decision:** A task is overdue only when its `due_date` is earlier than today and its status is not `Done`.


## Feature 2: Search + Combined Filters

### User Story 1 — Search by Title and Description

As a user, I want to search tasks by title or description, so that I can quickly find relevant tasks.

**Acceptance Criteria:**
1. `GET /tasks` accepts an optional `search` query parameter.
2. Search checks both the task `title` and `description`.
3. A match in either field includes the task in the results.
4. Partial text matches are supported.
5. The existing task response format remains unchanged.

### User Story 2 — Case-Insensitive Search

As a user, I want search to ignore uppercase and lowercase differences, so that I can find tasks regardless of how their text was entered.

**Acceptance Criteria:**
1. Searching for `bug` can match `bug`, `Bug`, and `BUG`.
2. Mixed-case search input returns the same matching tasks.
3. Case-insensitive matching applies to both `title` and `description`.
4. No matching tasks returns HTTP 200 with an empty list.

### User Story 3 — Combine Search and Filters

As a user, I want to combine search with status and priority filters, so that I can narrow the board to the tasks I need.

**Acceptance Criteria:**
1. Existing `status` and `priority` filters continue to work without search.
2. `search`, `status`, and `priority` can be used together.
3. Different filter types use AND logic.
4. A task must satisfy all active filters to appear.
5. No matching tasks returns HTTP 200 with an empty list.

### User Story 4 — Validate Filter Inputs

As an API client, I want invalid filter values to be rejected with clear validation errors, so that invalid requests are handled predictably.

**Acceptance Criteria:**
1. An invalid `status` filter returns HTTP 422.
2. An invalid `priority` filter returns HTTP 422.
3. The validation response identifies the invalid filter field.
4. Valid search text does not produce HTTP 422 because of letter casing.
5. Existing validation behavior remains unchanged.

### User Story 5 — Search and Filter the Kanban Board

As a user, I want a compact search and filter bar above the Kanban board, so that I can refine visible tasks without losing the board context.

**Acceptance Criteria:**
1. A compact search/filter bar appears above the Kanban columns.
2. It contains controls for search text, status, and priority.
3. The controls can be used individually or together.
4. Applying the controls updates the tasks displayed on the board.
5. All Kanban columns remain visible when no tasks match.
6. Empty columns continue to display their normal empty state.

### AI Assumption Corrected

Copilot initially used `developer` as the role for the filter-validation user story.

I changed the role to `API client` because the story describes the behavior experienced by a caller of the API rather than a development activity.

**Final decision:** Invalid `status` or `priority` filter values should return HTTP 422 with clear validation information.