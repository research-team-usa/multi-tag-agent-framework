"""Bounded stack with overflow protection."""

from collections import deque
from typing import Any, Deque

class AmplifierStack:
    """Stack that holds max 5 items – prevents runaway amplification."""

    def __init__(self, max_size: int = 5) -> None:
        self.max_size = max_size
        self._stack: Deque[Any] = deque(maxlen=max_size)

    def push(self, item: Any) -> None:
        """Push item, raise if overflow would occur."""
        if len(self._stack) >= self.max_size:
            raise OverflowError("AmplifierStack overflow – max 5 items")
        self._stack.append(item)

    def pop(self) -> Any:
        """Pop last item."""
        return self._stack.pop()

    def __len__(self) -> int:
        return len(self._stack)
