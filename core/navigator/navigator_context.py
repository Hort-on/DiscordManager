from typing import Any

from core.navigator.routes import Route


class NavigationContext:
    def __init__(self):
        self.stack: list[tuple[Route, Any | None]] = []

    def push(self, target: Route, params: Any | None = None):
        self.stack.append((target, params))

    def pop(self):
        if not self.stack:
            return None
        return self.stack.pop()
