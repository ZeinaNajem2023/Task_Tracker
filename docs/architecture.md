# Architecture Context Strategy Comparison

## 1. Strategy comparison

| Strategy | What it got right | What it got wrong, missed, or invented | Best-suited task shape |
|---|---|---|---|
| **A — Minimal context** | Produced the most complete and internally consistent account. It connected the Kanban frontend to the FastAPI CRUD API, described the creation flow end to end, documented validation and in-memory storage, and clearly separated confirmed details from assumptions. | Its accuracy depended on broad repository inspection rather than the initial prompt alone. “Kanban board” was explicitly identified as an inference, while frontend serving and production behavior remained unconfirmed. | Open-ended architecture or repository-understanding tasks where the relevant files are not known in advance and direct inspection is allowed. |
| **B — Structured context** | Quickly established the stack, major components, business rules, CORS setup, and intended file responsibilities. It also noticed that the supplied file-summary context was incomplete. | It included due dates, overdue filtering, search, and test files even though the same output acknowledged that those files were absent during inspection. This made the draft internally inconsistent and allowed stale or unsupported structured context to override stronger evidence. | Fast orientation and documentation when the supplied structural summary is current, complete, and trusted—or when the task is to describe intended architecture rather than verified implementation. |
| **C — Targeted context** | Stayed disciplined about its evidence boundary. It accurately described the API models, CRUD request flow, validation, UUID/timestamp creation, in-memory dictionary, and 404 behavior while repeatedly marking unseen details as “not visible from the files I read.” | It could not describe the frontend workflow, exact transition rules, health response, tests, deployment, or broader project structure. Its key-files section named imported files but could not explain their implementations, so the result was cautious but incomplete. | Focused analysis of a known subsystem, request path, or change area where a few anchor files contain the necessary evidence and limiting inspection is important. |

## 2. Verdict

I chose **Strategy A** for the final architecture document because it produced the most complete, evidence-based, and internally consistent description of the application. Strategy C was more rigorous about uncertainty but missed important cross-component behavior, while Strategy B introduced claims that its own assumptions section identified as unverified or inconsistent with the inspected repository state.

## 3. Context-engineering rule

For an open-ended repository architecture task, I use **Strategy A** because inspecting the relevant files as they are discovered gives the best balance of coverage, accuracy, and explicit uncertainty. For a narrowly scoped subsystem or request-flow task, I use **Strategy C** because a small set of anchor files limits noise and makes the boundary between confirmed and unseen behavior clear.
