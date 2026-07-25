# Verification

## Baseline Check

Before making feature changes, I checked the existing application.

Results:

- `pytest` completed successfully but collected `0` tests because the project did not yet contain pytest-style test files.
- The `/health` endpoint returned HTTP 200.
- The existing Kanban frontend loaded successfully.

This established the baseline before implementing the two features.

## Backend Test Results

After implementing Due Dates + Overdue Filtering and Search + Combined Filters, I ran the full pytest suite.

Command:

`python -m pytest -q`

Result:

`9 passed`

The tests cover:

- valid and invalid due dates
- updating and clearing due dates
- overdue filtering
- title and description search
- case-insensitive search
- combined filters
- empty search results

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

Before final cleanup, I verified the expected behavior of both features.

The behavior contract included:

- Existing task creation and update behavior still works.
- Due dates can be created, updated, and cleared.
- Tasks due today are not overdue.
- `Done` tasks are never overdue.
- Search works on title and description.
- Search is case-insensitive.
- Search, status, priority, and overdue filters combine using AND logic.
- Empty results return HTTP 200 with an empty list.
- All Kanban columns remain visible when filters return no tasks.

Full test result:

`9 passed`

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

The full test suite was rerun and returned:

`9 passed`
