# Verification

## Baseline Check

Before making feature changes, I checked the existing application.

Results:

- `pytest` initially collected `0` tests because the project did not yet contain pytest-style baseline tests.
- The `/health` endpoint returned HTTP 200.
- The existing Kanban frontend loaded successfully.

For the revision, I added automated baseline pytest coverage for the existing application behavior, including:

- create and get task
- list tasks
- update task
- delete task
- missing-task 404 responses
- valid status transitions
- invalid status transitions

Baseline test result:

`10 passed`

## Backend Test Results

After adding the baseline tests and keeping the Feature 1 and Feature 2 tests, I ran the full pytest suite.

Command:

`python -m pytest -q`

Result:

`16 passed`

The full suite now covers both the original CRUD/status-transition behavior and the two new features.

## Manual Browser Checks

I manually verified the frontend behavior.

Checks included:

- Creating a task with a due date.
- Displaying the due date on the Kanban card.
- Displaying `No due date` when no date is provided.
- Confirming overdue tasks receive the overdue visual indicator.
- Confirming tasks due today are not overdue.
- Confirming `Done` tasks are not marked overdue.
- Searching tasks using the search bar.
- Testing case-insensitive search.
- Filtering by status and priority.
- Combining search, status, priority, and overdue filters.
- Confirming all Kanban columns remain visible when no tasks match.

## Behavior Contract

The behavior contract includes:

- Existing create, get, list, update, and delete behavior works.
- Valid status transitions are accepted.
- Invalid status transitions are rejected.
- Due dates can be created, updated, and cleared.
- Tasks due today are not overdue.
- `Done` tasks are never overdue.
- Search works on title and description.
- Search is case-insensitive.
- Search, status, priority, and overdue filters combine using AND logic.
- Empty results return HTTP 200 with an empty list.
- All Kanban columns remain visible when filters return no tasks.

Final full test result:

`16 passed`

## Break Test 1 — Overdue Detection

**Intentional break:**  
Changed the overdue comparison in `app/storage.py` from:

`due_date < today`

to:

`due_date <= today`

This intentionally introduced a bug where tasks due today were incorrectly treated as overdue.

**Expected result:**  
`test_overdue_filter_returns_only_overdue_non_done_tasks` should fail.

**Observed result:**  
1 test failed and 3 passed.

The failing test was:

`test_overdue_filter_returns_only_overdue_non_done_tasks`

**Conclusion:**  
The test correctly detected the broken overdue rule and proved that tasks due today are protected from being incorrectly classified as overdue.

After the Break Test, the production code was restored to:

`due_date < today`

The Feature 1 test suite was rerun and returned:

`4 passed`

## Break Test 2 — Case-Insensitive Search

**Intentional break:**  
Removed `.lower()` from the task title and description comparison in `app/storage.py`.

The correct code:

`normalized_search in task.title.lower() or normalized_search in task.description.lower()`

was temporarily changed to:

`normalized_search in task.title or normalized_search in task.description`

This intentionally broke case-insensitive search, so a search such as `bug` no longer reliably matched text such as `BUG triage`.

**Expected result:**  
The Feature 2 search tests should fail.

**Observed result:**  
2 tests failed and 3 passed.

**Conclusion:**  
The tests correctly detected that case-insensitive search behavior had been broken.

After the Break Test, the correct `.lower()` comparisons were restored.

The final full test suite was rerun and returned:

`16 passed`
