# Comments on Tasks Feature Plan

## 1. Data Model

Add comment request and response models to `app/models.py`, following the existing separation between client-supplied fields (`TaskCreate`, `TaskUpdate`) and server-generated response fields (`TaskResponse`).

### `CommentCreate`

- `author`: required string, 1–100 characters.
- `body`: required string, 1–2000 characters.
- Use Pydantic v2 validation and `ConfigDict(extra="forbid")`, consistent with the existing task request models.
- Reject missing, blank, and whitespace-only values.
- Do not accept `id`, `task_id`, or `created_at` from clients.

The existing `TaskCreate.validate_title` validator strips surrounding whitespace before checking whether a title is blank or too long. The comment author should follow that convention. Whether the body should also be trimmed is an open decision because surrounding whitespace could be intentional content.

### `CommentResponse`

- `id`: string containing a server-generated UUID.
- `task_id`: string referencing the parent task.
- `author`: validated author string.
- `body`: validated body string.
- `created_at`: server-generated, timezone-aware UTC `datetime`.
- Use `ConfigDict(extra="forbid")`, consistent with `TaskResponse`.

Keep comments separate from `TaskResponse`. Embedding them would change all existing task responses and make `GET /tasks` return potentially unnecessary comment data.

Comment field validation belongs in `app/models.py`, following the conventions documented in `AGENTS.md` and `README.md`. No change to `app/business_rules.py` is needed unless additional comment lifecycle rules are introduced.

## 2. API Routes

Task routes currently live directly in `app/main.py`; only the health endpoint uses a router. The initial comment routes should follow that convention unless route organization is refactored separately.

### Create a comment

- **Method:** `POST`
- **Path:** `/tasks/{task_id}/comments`
- **Request body:** `CommentCreate`, containing `author` and `body`.
- **Success status:** `201 Created`.
- **Response body:** `CommentResponse`, containing `id`, `task_id`, `author`, `body`, and `created_at`.

The route should confirm that the task exists, take `task_id` from the path, generate a UUID string for `id`, and generate `created_at` using a timezone-aware UTC value. This matches the `uuid4()` and `datetime.now(timezone.utc)` conventions in `app/storage.py`.

Error cases:

- `404 Not Found` if the task does not exist. For consistency with current routes, use the detail format `Task with id {task_id} not found`.
- `422 Unprocessable Entity` if `author` or `body` is missing, blank, whitespace-only, or too long.
- `422 Unprocessable Entity` for unknown fields or attempts to submit server-controlled fields such as `id`, `task_id`, or `created_at`.

### List comments for a task

- **Method:** `GET`
- **Path:** `/tasks/{task_id}/comments`
- **Request body:** none.
- **Success status:** `200 OK`.
- **Response body:** a list of `CommentResponse` objects.

Recommended behavior:

- Return only comments belonging to the specified task.
- Return an empty list when the task exists but has no comments, matching the empty-list behavior of `GET /tasks`.
- Return `404 Not Found` when the parent task does not exist.
- Guarantee a documented order. Oldest-first by `created_at` is recommended for conversational reading.

### Routes outside the initial scope

Do not initially add get-by-comment-ID, update, or delete routes unless the team confirms those requirements. The requested shape has no `updated_at`, which suggests comments may be immutable.

Existing task routes treat path IDs as unrestricted strings and return `404` when no resource matches. Comment routes should retain that behavior unless task and comment path parameters are deliberately changed to UUID-typed parameters.

## 3. Tests

Add API tests in a focused module such as `tests/test_comments.py`.

Follow the conventions visible in `tests/test_baseline_crud.py`:

- Use FastAPI's `TestClient`.
- Exercise behavior through HTTP requests.
- Assert response status codes and JSON fields directly.
- Use the autouse fixture that calls `storage._reset()` before and after each test.
- Group tests by endpoint or behavior.
- Run the suite with the repository-standard `pytest -v`.

The storage reset operation must clear comments as well as tasks so comment tests and existing CRUD tests remain isolated.

### Happy path

- `test_create_comment_returns_201`
- `test_create_comment_returns_expected_fields`
- `test_create_comment_generates_uuid_id`
- `test_create_comment_uses_route_task_id`
- `test_create_comment_sets_utc_created_at`
- `test_list_comments_empty`
- `test_list_comments_returns_created_comments`
- `test_list_comments_returns_oldest_first`
- `test_list_comments_only_returns_comments_for_requested_task`

### Validation

- `test_create_comment_missing_author_rejected`
- `test_create_comment_blank_author_rejected`
- `test_create_comment_whitespace_author_rejected`
- `test_create_comment_author_at_100_characters_accepted`
- `test_create_comment_author_over_100_characters_rejected`
- `test_create_comment_missing_body_rejected`
- `test_create_comment_blank_body_rejected`
- `test_create_comment_whitespace_body_rejected`
- `test_create_comment_body_at_2000_characters_accepted`
- `test_create_comment_body_over_2000_characters_rejected`
- `test_create_comment_extra_field_rejected`
- `test_create_comment_client_id_rejected`
- `test_create_comment_client_task_id_rejected`
- `test_create_comment_client_created_at_rejected`

If trimming is selected:

- `test_create_comment_trims_author`
- `test_create_comment_trims_body`

### Edge cases

- `test_create_comment_task_not_found`
- `test_list_comments_task_not_found`
- `test_storage_reset_clears_comments`
- `test_comment_created_at_cannot_be_overridden`
- `test_existing_task_responses_do_not_embed_comments`
- `test_deleting_task_removes_its_comments`, if cascade deletion is selected.
- `test_deleting_task_does_not_remove_other_task_comments`

`tests/verify_a.py` is a manual, print-based validation script rather than a normal pytest test module. Automated comment coverage should follow `tests/test_baseline_crud.py`.

## 4. Frontend Changes

All current frontend markup, styling, and JavaScript are contained in `frontend/index.html`. No separate task-detail page or comments interface is visible in the repository.

Recommended changes to `frontend/index.html`:

- Add a Comments button beside the existing Edit button on each task card.
- Open a dedicated comments modal or side panel for the selected task.
- Display the selected task title and its existing comments.
- Display each comment's author, formatted creation time, and body.
- Show an empty-state message when no comments exist.
- Add a form with a required author input and required body textarea.
- Show the 100- and 2000-character limits and accessible validation errors.
- Fetch comments from `GET /tasks/{task_id}/comments` when the comments interface opens.
- Submit comments to `POST /tasks/{task_id}/comments`.
- Append the returned comment or reload the list after successful creation.
- Disable submission while the request is pending to reduce duplicate submissions.
- Provide loading, empty, ready, validation-error, submission-error, and network-error states.
- Reuse or generalize the existing `parseErrorMessage` behavior for FastAPI error payloads.
- Pass author and body through the existing `escapeHtml` helper before generated HTML insertion.
- Preserve body line breaks without treating comment content as trusted HTML.
- Leave task creation, editing, board rendering, and drag-and-drop behavior unchanged.

A separate comments modal or panel is preferable to extending the task form because the current modal is tightly coupled to create/edit state and clears that state when closed.

No frontend testing framework is visible. UI behavior will require manual verification unless browser or JavaScript tests are separately approved.

## 5. Migration Notes

`app/storage.py` currently uses a module-level in-memory dictionary keyed by task ID. There is no database, persistent storage, or migration framework.

For the current architecture:

- Add a separate in-memory comment collection rather than embedding comments in `TaskResponse`.
- Key comments by comment ID or maintain a mapping from task IDs to comment collections.
- Ensure storage operations can list comments for one task.
- Confirm task existence before storing a comment.
- Extend `storage._reset()` to clear comment state.
- Do not rewrite existing task records or add embedded empty comment lists.
- Keep existing task endpoint response shapes unchanged.
- Comments, like tasks, will be lost when the process restarts.

Task deletion requires an explicit rule. Cascade-deleting associated comments is recommended because it prevents unreachable records and approximates foreign-key cascade behavior in the current in-memory design.

There is no real foreign-key mechanism in the current storage layer. Referential integrity must be enforced by application storage operations. If database persistence is introduced later, comments would require a table or equivalent collection, a task reference, an index on `task_id`, and a defined deletion constraint. Database work is outside the repository's documented scope.

## 6. Open Questions

1. Should deleting a task cascade-delete its comments, prevent deletion, or retain them through another policy?
2. Are comments immutable, or will editing be required later?
3. Should users be able to delete comments?
4. Should surrounding whitespace be trimmed from both fields, or only from `author`?
5. Should comments be returned oldest-first or newest-first?
6. Should task cards display comment counts? Adding counts to task responses would change the existing task API shape, while fetching per-card counts could require many requests.
7. Should the comments interface be a modal, side panel, or future task-detail view?
8. Should malformed UUID-like path values continue to produce `404`, following current task-ID behavior, or be rejected with `422`?
9. Is an unbounded comment list acceptable, or is pagination required?
10. Is free-form `author` text intentional, given that the application has no authentication?
11. Should comment creation update the parent task's `updated_at` value?

# Files read

- `AGENTS.md`
- `README.md`
- `app/models.py`
- `app/main.py`
- `app/storage.py`
- `app/routers/health.py`
- `app/routers/__init__.py`
- `tests/test_baseline_crud.py`
- `tests/verify_a.py`
- `frontend/index.html`
- Repository file listings under `app/`, `tests/`, and the project root.

`AGENTS.md` references `tests/test_feature1_due_date.py` and `tests/test_feature2_search.py`, but those files were not present in the repository listing and therefore could not be inspected.

# Assumptions to verify

- **Assumption:** The initial feature includes comment creation and listing only.
- **Assumption:** Comments remain separate from `TaskResponse`.
- **Assumption:** Whitespace-only author and body values are invalid.
- **Assumption:** Comment lists are returned oldest first.
- **Assumption:** Deleting a task cascade-deletes its comments.
- **Assumption:** Listing comments for a nonexistent task returns `404`, while listing comments for an existing task with none returns an empty list.
- **Assumption:** Comment IDs remain strings in API models but contain valid UUID values.
- **Assumption:** The existing unrestricted string path-ID convention remains unchanged.
- **Assumption:** Comment creation does not modify the task's `updated_at`.
- **Assumption:** Authentication, database persistence, deployment work, and major UI redesign are outside this feature's scope.
- **Assumption:** Frontend verification remains manual because no browser or JavaScript test framework is visible.
