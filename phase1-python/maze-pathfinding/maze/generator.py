import random
from maze.grid import Grid, Position, CellType


def generate(rows: int, cols: int, loop_factor: float = 0.15) -> tuple[Grid, Position, Position]:
    """
    Generate a maze using Recursive Backtracker (DFS),
    then add loops by removing extra walls for visual density.

    Args:
        rows: Grid height (must be odd).
        cols: Grid width (must be odd).
        loop_factor: Fraction of interior walls to remove after generation.
                     0.0 = perfect maze, 0.3 = dense with many loops.

    Returns:
        The grid, start position, and end position.
    """
    rows = rows if rows % 2 != 0 else rows + 1
    cols = cols if cols % 2 != 0 else cols + 1
    grid = Grid(rows, cols)

    start = Position(1, 1)
    end = Position(rows - 2, cols - 2)

    _carve_iterative(grid, start)
    _add_loops(grid, loop_factor)

    grid.set(start, CellType.START)
    grid.set(end, CellType.END)

    return grid, start, end


def _carve_iterative(grid: Grid, start: Position) -> None:
    """
    Iterative Recursive Backtracker using an explicit stack.
    Avoids Python's recursion limit for large mazes.
    """
    grid.set(start, CellType.PATH)
    stack: list[Position] = [start]

    while stack:
        current = stack[-1]
        unvisited = [
            n for n in _get_carve_neighbors(grid, current)
            if grid.is_wall(n)
        ]

        if unvisited:
            neighbor = random.choice(unvisited)
            wall_between = _wall_between(current, neighbor)
            grid.set(wall_between, CellType.PATH)
            grid.set(neighbor, CellType.PATH)
            stack.append(neighbor)
        else:
            stack.pop()


def _add_loops(grid: Grid, loop_factor: float) -> None:
    """Remove a fraction of interior walls to create loops and alternate paths."""
    if loop_factor <= 0:
        return

    interior_walls = [
        Position(r, c)
        for r in range(1, grid.rows - 1)
        for c in range(1, grid.cols - 1)
        if grid.is_wall(Position(r, c))
        and _has_path_neighbors(grid, Position(r, c))
    ]

    count = int(len(interior_walls) * loop_factor)
    for pos in random.sample(interior_walls, min(count, len(interior_walls))):
        grid.set(pos, CellType.PATH)


def _has_path_neighbors(grid: Grid, pos: Position) -> bool:
    """Only remove walls adjacent to at least 2 path cells — avoids isolated openings."""
    path_neighbors = sum(
        1 for n in pos.neighbors()
        if grid.in_bounds(n) and not grid.is_wall(n)
    )
    return path_neighbors >= 2


def _get_carve_neighbors(grid: Grid, pos: Position) -> list[Position]:
    candidates = [
        Position(pos.row - 2, pos.col),
        Position(pos.row + 2, pos.col),
        Position(pos.row, pos.col - 2),
        Position(pos.row, pos.col + 2),
    ]
    return [n for n in candidates if grid.in_bounds(n)]


def _wall_between(a: Position, b: Position) -> Position:
    return Position(
        (a.row + b.row) // 2,
        (a.col + b.col) // 2,
    )
