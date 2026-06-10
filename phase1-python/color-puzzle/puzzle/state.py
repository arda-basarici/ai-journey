from __future__ import annotations
from collections import deque
from dataclasses import dataclass
from puzzle.board import Board, Position


@dataclass(frozen=True)
class ColorState:
    head: Position
    tail: Position
    path: tuple[Position, ...]
    connected: bool


class PuzzleState:
    """
    Immutable snapshot of solving progress.
    Each instance is one node in the A* search graph.

    Design principles:
    - 'occupied' holds cells claimed by path heads (starts only initially)
    - Tail endpoints are unoccupied targets until a color connects
    - A color connects by stepping into its tail cell
    - Two pruning rules keep the search tractable:
        1. No empty cell becomes isolated (unreachable by any head)
        2. Every unconnected head can still reach its tail via BFS
    """

    def __init__(
        self,
        board: Board,
        color_states: dict[str, ColorState],
        occupied: frozenset[Position],
    ):
        self.board = board
        self.color_states = color_states
        self.occupied = occupied
        self._hash: int | None = None

    @classmethod
    def initial(cls, board: Board) -> "PuzzleState":
        color_states = {
            pair.name: ColorState(
                head=pair.start,
                tail=pair.end,
                path=(pair.start,),
                connected=False,
            )
            for pair in board.colors
        }
        occupied = frozenset(pair.start for pair in board.colors)
        return cls(board, color_states, occupied)

    def is_solved(self) -> bool:
        all_connected = all(cs.connected for cs in self.color_states.values())
        all_filled = len(self.occupied) == self.board.total_cells
        return all_connected and all_filled

    def _tails(self, states: dict | None = None) -> frozenset[Position]:
        cs = states or self.color_states
        return frozenset(c.tail for c in cs.values() if not c.connected)

    def heuristic(self) -> int:
        tails = self._tails()
        dist = sum(
            cs.head.distance_to(cs.tail)
            for cs in self.color_states.values()
            if not cs.connected
        )
        free = self.board.total_cells - len(self.occupied) - len(tails)
        return dist + max(0, free)

    def _is_valid(
        self,
        new_occupied: frozenset[Position],
        new_color_states: dict,
    ) -> bool:
        """
        Two pruning checks after a move:
        1. No empty non-tail cell is completely surrounded
        2. Every unconnected head can reach its tail via BFS
        """
        new_tails = self._tails(new_color_states)
        new_heads = frozenset(
            cs.head for cs in new_color_states.values() if not cs.connected
        )

        # Check 1: no isolated empty cells
        for r in range(self.board.size):
            for c in range(self.board.size):
                pos = Position(r, c)
                if pos in new_occupied or pos in new_tails:
                    continue
                reachable = any(
                    nb in new_heads
                    or (self.board.in_bounds(nb)
                        and nb not in new_occupied
                        and nb not in new_tails)
                    for nb in pos.neighbors()
                    if self.board.in_bounds(nb)
                )
                if not reachable:
                    return False

        # Check 2: every head can reach its tail
        for cs in new_color_states.values():
            if cs.connected:
                continue
            if not self._bfs(cs.head, cs.tail, new_occupied, new_tails):
                return False

        return True

    def _bfs(
        self,
        start: Position,
        target: Position,
        occupied: frozenset[Position],
        tails: frozenset[Position],
    ) -> bool:
        if start == target:
            return True
        queue = deque([start])
        seen = {start}
        while queue:
            cur = queue.popleft()
            for nb in cur.neighbors():
                if not self.board.in_bounds(nb):
                    continue
                if nb == target:
                    return True
                if nb not in seen and nb not in occupied and nb not in tails:
                    seen.add(nb)
                    queue.append(nb)
        return False

    def next_states(self) -> list["PuzzleState"]:
        unconnected = [
            name for name, cs in self.color_states.items()
            if not cs.connected
        ]
        if not unconnected:
            return []

        tails = self._tails()

        def moves_available(name: str) -> int:
            cs = self.color_states[name]
            return sum(
                1 for nb in cs.head.neighbors()
                if self.board.in_bounds(nb)
                and (nb == cs.tail or (nb not in self.occupied and nb not in tails))
            )

        # Extend most constrained color first
        name = min(unconnected, key=moves_available)
        cs = self.color_states[name]
        states = []

        for nb in cs.head.neighbors():
            if not self.board.in_bounds(nb):
                continue

            is_tail = nb == cs.tail
            if not is_tail and (nb in self.occupied or nb in tails):
                continue

            new_cs = ColorState(
                head=nb,
                tail=cs.tail,
                path=cs.path + (nb,),
                connected=is_tail,
            )
            new_color_states = {**self.color_states, name: new_cs}
            new_occupied = self.occupied | {nb}

            if self._is_valid(new_occupied, new_color_states):
                states.append(PuzzleState(self.board, new_color_states, new_occupied))

        return states

    def __hash__(self) -> int:
        if self._hash is None:
            object.__setattr__(self, '_hash', hash((
                tuple(sorted(
                    (name, cs.head, cs.connected)
                    for name, cs in self.color_states.items()
                )),
                self.occupied,
            )))
        return self._hash

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PuzzleState):
            return False
        return (self.occupied == other.occupied
                and self.color_states == other.color_states)
