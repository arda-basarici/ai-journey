import heapq
from typing import TypeVar, Generic

T = TypeVar("T")


class PriorityQueue(Generic[T]):
    """Min-heap priority queue wrapping Python's heapq."""

    def __init__(self):
        self._heap: list[tuple[float, int, T]] = []
        self._counter: int = 0

    def push(self, item: T, priority: float) -> None:
        heapq.heappush(self._heap, (priority, self._counter, item))
        self._counter += 1

    def pop(self) -> T:
        _, _, item = heapq.heappop(self._heap)
        return item

    def is_empty(self) -> bool:
        return len(self._heap) == 0
