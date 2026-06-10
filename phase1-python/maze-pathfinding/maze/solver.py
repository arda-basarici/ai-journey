from collections.abc import Callable
from maze.grid import Grid, Position
from utils.heap import PriorityQueue


def solve(
    grid: Grid,
    start: Position,
    end: Position,
    on_open: Callable[[Position], None] | None = None,
    on_close: Callable[[Position], None] | None = None,
) -> list[Position] | None:
    """
    A* pathfinding algorithm.

    Args:
        grid: The maze grid.
        start: Starting position.
        end: Target position.
        on_open: Callback fired when a cell is added to the frontier (open set).
        on_close: Callback fired when a cell is popped and processed (closed set).

    Returns:
        List of positions forming the path from start to end,
        or None if no path exists.
    """
    frontier: PriorityQueue[Position] = PriorityQueue()
    frontier.push(start, 0)

    came_from: dict[Position, Position | None] = {start: None}
    cost_so_far: dict[Position, float] = {start: 0}
    open_set: set[Position] = {start}
    closed_set: set[Position] = set()

    while not frontier.is_empty():
        current = frontier.pop()
        open_set.discard(current)
        closed_set.add(current)

        if current not in (start, end) and on_close:
            on_close(current)

        if current == end:
            return _reconstruct_path(came_from, start, end)

        for neighbor in grid.walkable_neighbors(current):
            if neighbor in closed_set:
                continue

            new_cost = cost_so_far[current] + 1

            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + neighbor.distance_to(end)
                frontier.push(neighbor, priority)
                came_from[neighbor] = current

                if neighbor not in open_set:
                    open_set.add(neighbor)
                    if neighbor not in (start, end) and on_open:
                        on_open(neighbor)

    return None


def _reconstruct_path(
    came_from: dict[Position, Position | None],
    start: Position,
    end: Position,
) -> list[Position]:
    path: list[Position] = []
    current: Position | None = end

    while current is not None:
        path.append(current)
        current = came_from.get(current)

    path.reverse()
    return path
