from dataclasses import dataclass


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
        """Manhattan distance — used as A* heuristic."""
        return abs(self.row - other.row) + abs(self.col - other.col)


@dataclass(frozen=True)
class ColorPair:
    name: str
    start: Position
    end: Position


class Board:
    """
    Immutable puzzle definition.
    Holds grid size and color endpoint pairs only.
    No solving state lives here.
    """

    def __init__(self, size: int, colors: list[ColorPair]):
        self.size = size
        self.colors = colors
        self._endpoints: frozenset[Position] = frozenset(
            pos
            for pair in colors
            for pos in (pair.start, pair.end)
        )

    def in_bounds(self, pos: Position) -> bool:
        return 0 <= pos.row < self.size and 0 <= pos.col < self.size

    def is_endpoint(self, pos: Position) -> bool:
        return pos in self._endpoints

    @property
    def total_cells(self) -> int:
        return self.size * self.size

