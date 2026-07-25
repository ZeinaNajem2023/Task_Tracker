# AI Reflection

During this mid-course project, I used GitHub Copilot to inspect my Task Tracker code, suggest small changes, generate diffs, and help with backend, frontend, and pytest updates. I used it mainly inside VS Code while working directly with the project files.

One moment where Copilot helped me was with the due date and overdue feature. It suggested using an optional Python `date` field and computing overdue status dynamically instead of storing an `is_overdue` value. This kept the solution simple and avoided unnecessary complexity or stale data. It also helped me extend the existing `GET /tasks` endpoint instead of creating new endpoints that were not needed.

Copilot also slowed me down during testing because different virtual environments were used and some were missing packages such as `pytest` and `httpx`. This caused errors that were related to the environment rather than the feature itself. I had to inspect which Python interpreter was active, switch to the correct virtual environment, and verify the dependencies before continuing.

One important place where my review changed the result was the overdue rule. Copilot initially described the completion condition too generally, but I inspected the existing project and confirmed that the exact statuses are `ToDo`, `InProgress`, and `Done`. I corrected the rule so that a task is overdue only when `due_date < today` and status is not `Done`.

I verified this with a Break Test by intentionally changing `<` to `<=`. The related test failed, proving that the test correctly protected the intended rule. I also used another Break Test to verify case-insensitive search.

Overall, Copilot helped me work faster by inspecting the existing code, suggesting focused changes, and supporting implementation. However, I still needed to inspect, review, test, and verify every important change before accepting it.
