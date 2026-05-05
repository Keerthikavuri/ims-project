from abc import ABC, abstractmethod


# Strategy Pattern — Base
class AlertStrategy(ABC):
    @abstractmethod
    def get_priority(self) -> str:
        pass

    @abstractmethod
    def get_message(self, component_id: str) -> str:
        pass


# P0 — Critical (RDBMS, MCP)
class CriticalAlertStrategy(AlertStrategy):
    def get_priority(self) -> str:
        return "P0"

    def get_message(self, component_id: str) -> str:
        return f"CRITICAL: {component_id} is down! Immediate action required."


# P1 — High (API, QUEUE)
class HighAlertStrategy(AlertStrategy):
    def get_priority(self) -> str:
        return "P1"

    def get_message(self, component_id: str) -> str:
        return f"HIGH: {component_id} is degraded! Investigate immediately."


# P2 — Medium (CACHE, NOSQL)
class MediumAlertStrategy(AlertStrategy):
    def get_priority(self) -> str:
        return "P2"

    def get_message(self, component_id: str) -> str:
        return f"MEDIUM: {component_id} has issues. Monitor closely."


# Factory —
def get_alert_strategy(component_type: str) -> AlertStrategy:
    mapping = {
        "RDBMS": CriticalAlertStrategy(),
        "MCP": CriticalAlertStrategy(),
        "API": HighAlertStrategy(),
        "QUEUE": HighAlertStrategy(),
        "CACHE": MediumAlertStrategy(),
        "NOSQL": MediumAlertStrategy(),
    }
    return mapping.get(component_type.upper(), MediumAlertStrategy())