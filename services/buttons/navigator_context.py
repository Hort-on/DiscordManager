class NavigationContext:
    def __init__(self):
        self.stack: list[tuple[str, dict | None]] = []

    def push(self, target: str, params: dict | None = None):
        self.stack.append((target, params))

    def pop(self):
        if not self.stack:
            return None
        return self.stack.pop()

