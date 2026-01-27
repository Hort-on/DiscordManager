from typing import Any


class NavigationContext:
    def __init__(self):
        self.stack: list[tuple[str, dict]] = []

    def back_view(self, target: str, params: dict[str, Any]) -> None:
        self.stack.append((target, params))

    def pop(self) -> tuple[str, dict] | None:
        if len(self.stack) <= 1:
            return None
        self.stack.pop()
        return self.stack[-1]
