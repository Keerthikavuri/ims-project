from enum import Enum


# State Pattern — Valid States
class WorkItemStatus(str, Enum):
    OPEN = "OPEN"
    INVESTIGATING = "INVESTIGATING"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"


# Valid transitions map
VALID_TRANSITIONS = {
    WorkItemStatus.OPEN: [WorkItemStatus.INVESTIGATING],
    WorkItemStatus.INVESTIGATING: [WorkItemStatus.RESOLVED],
    WorkItemStatus.RESOLVED: [WorkItemStatus.CLOSED],
    WorkItemStatus.CLOSED: [],
}


class StateMachine:
    def __init__(self, current_status: str):
        self.current = WorkItemStatus(current_status)

    def can_transition(self, new_status: str) -> bool:
        try:
            target = WorkItemStatus(new_status)
            return target in VALID_TRANSITIONS[self.current]
        except ValueError:
            return False

    def transition(self, new_status: str) -> str:
        if not self.can_transition(new_status):
            raise ValueError(
                f"Invalid transition: {self.current} -> {new_status}. "
                f"Allowed: {[s.value for s in VALID_TRANSITIONS[self.current]]}"
            )
        self.current = WorkItemStatus(new_status)
        return self.current.value