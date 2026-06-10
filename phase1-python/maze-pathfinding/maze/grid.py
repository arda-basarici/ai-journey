from dataclasses import dataclass
from enum import Enum


class CellType(Enum):
    WALL  = "#"
    PATH  = " "
    START = "S"
    END   = "E"


@dataclass(frozen=True)
class Position:
    row: int
    col: int

    def neighbors(self) -> list["Position"]:
        return [
            Position(self.row - 1, self.col),
            Position(self.row + 1, self.col),
            Position(self.row, self.col - 1),
            Position(self.row, self.col + 1),
        ]

    def distance_to(self, other: "Position") -> int:
        """Manhattan distance heuristic for A*."""
        return abs(self.row - other.row) + abs(self.col - other.col)


class Grid:
    def __init__(self, rows: int, cols: int):
        if rows % 2 == 0 or cols % 2 == 0:
            raise ValueError("Grid dimensions must be odd for maze generation.")
        self.rows = rows
        self.cols = cols
        self._cells: list[list[CellType]] = [
            [CellType.WALL for _ in range(cols)]
            for _ in range(rows)
        ]

    def get(self, pos: Position) -> CellType:
        return self._cells[pos.row][pos.col]

    def set(self, pos: Position, cell_type: CellType) -> None:
        self._cells[pos.row][pos.col] = cell_type

    def is_wall(self, pos: Position) -> bool:
        return self._cells[pos.row][pos.col] == CellType.WALL

    def in_bounds(self, pos: Position) -> bool:
        return 0 <= pos.row < self.rows and 0 <= pos.col < self.cols

    def walkable_neighbors(self, pos: Position) -> list[Position]:
        return [
            n for n in pos.neighbors()
            if self.in_bounds(n) and not self.is_wall(n)
        ]
