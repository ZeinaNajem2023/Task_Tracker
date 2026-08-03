from fastapi import HTTPException, status

from app.models import TaskStatus

VALID_TRANSITIONS: frozenset[tuple[TaskStatus, TaskStatus]] = frozenset({
    (TaskStatus.TODO, TaskStatus.IN_PROGRESS),
    (TaskStatus.IN_PROGRESS, TaskStatus.DONE),
    (TaskStatus.DONE, TaskStatus.IN_PROGRESS),
})


def validate_status_transition(current: TaskStatus, new: TaskStatus) -> None:
    """Validate that a status change is allowed by business rules.

    Args:
        current: Existing task status.
        new: Requested next status.

    Returns:
        None.

    Raises:
        HTTPException: 422 when `(current, new)` is not in allowed transitions.

    Notes:
        Allowed transitions are:
        - ToDo -> InProgress
        - InProgress -> Done
        - Done -> InProgress
    """
    if (current, new) not in VALID_TRANSITIONS:
        allowed = sorted({f"{from_status.value}->{to_status.value}" for from_status, to_status in VALID_TRANSITIONS})
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid status transition from {current.value} to {new.value}. Allowed transitions: {allowed}",
        )
