## Break Test 1 — Overdue Detection

**Intentional break:**  
Changed the overdue comparison in `app/storage.py` from:

`due_date < today`

to:

`due_date <= today`

This incorrectly treated tasks due today as overdue.

**Expected result:**  
`test_overdue_filter_returns_only_overdue_non_done_tasks` should fail.

**Observed result:**  
1 test failed and 3 passed.

The failing test was:
`test_overdue_filter_returns_only_overdue_non_done_tasks`

**Conclusion:**  
The test correctly protects the overdue rule and detects when tasks due today are incorrectly classified as overdue.

After the Break Test, the production code was restored to `due_date < today` and the test suite was rerun.