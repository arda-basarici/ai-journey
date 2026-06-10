# Color Flow Puzzle — A\*

A\* search applied to an abstract state-space problem.
Solves Color Flow puzzles algorithmically — connect matching colors
without crossing paths, filling every cell on the board.

## The problem

```
┌─────┬─────┬─────┬─────┬─────┐
│  ●  │     │  ●  │     │  ●  │   pink · green · yellow
├─────┼─────┼─────┼─────┼─────┤
│     │     │  ●  │     │  ●  │   blue · orange
├─────┼─────┼─────┼─────┼─────┤
│     │     │     │     │     │
├─────┼─────┼─────┼─────┼─────┤
│     │  ●  │     │  ●  │     │
├─────┼─────┼─────┼─────┼─────┤
│     │  ●  │  ●  │  ●  │     │
└─────┴─────┴─────┴─────┴─────┘
```

Rules: connect each pair of matching endpoints with a path.
Paths cannot cross. Every cell must be filled.

This is an NP-complete constraint satisfaction problem —
the search space grows exponentially with grid size.

## How it works

### A\* on abstract state space

The core insight: A\* is a general search algorithm, not just
a pathfinding tool. By redefining what counts as a "node",
the same algorithm solves a completely different problem.

| Concept   | Maze pathfinding   | Color puzzle                         |
| --------- | ------------------ | ------------------------------------ |
| Node      | Grid position      | Entire board state                   |
| Neighbors | Adjacent cells     | Valid next board states              |
| Goal      | Reach end cell     | All colors connected + board full    |
| Heuristic | Manhattan distance | Σ distances to targets + empty cells |

### State design

Each `PuzzleState` is immutable and hashable — both required for A\*
correctness. It stores each color's current head position, tail target,
and path history.

**Two pruning rules** reject invalid states before they enter the frontier:

1. **No isolated cells** — if any empty cell becomes unreachable
   (surrounded by occupied cells with no color head adjacent),
   the state is pruned. That cell can never be filled.

2. **BFS reachability** — every unconnected color head must still
   be able to reach its tail through remaining empty cells.
   If any color is permanently cut off, prune immediately.

**Most-constrained-first** — at each step, the color with the fewest
valid moves is extended. This is the MRV heuristic from constraint
satisfaction — it catches dead ends early and avoids exploring branches
that are already doomed.

### Complexity

- 5×5: milliseconds
- 6×6: under 25ms
- 8×8: under 250ms
- 9×9: ~100ms
- Beyond ~10×10: exponential degradation — inherent to the NP-complete
  nature of the problem, not the implementation.

> A faster constraint propagation solver is planned for Phase 3,
> where both approaches will be benchmarked directly.

## Puzzle dataset

`levels/puzzles.json` contains 13 real puzzles taken from a deployed
Color Flow game. Every puzzle is
verified solvable by the A\* solver before inclusion.

Random puzzle generation was considered and prototyped but excluded —
generating guaranteed-solvable puzzles with good structure is itself
a hard problem (requires finding a Hamiltonian path, which is NP-complete).
Using real, well-designed puzzles produces a better demo.

## Usage

```bash
pip install -r requirements.txt
python main.py
```

Options:

```bash
python main.py --index 10    # specific puzzle by index (0–13)
python main.py --size 8      # random puzzle of given size
```

## Structure

```
color-puzzle/
  main.py           ← entry point
  puzzle/
    board.py        ← Board, Position, ColorPair (static puzzle)
    state.py        ← PuzzleState (A* node — immutable, hashable)
    solver.py       ← A* over puzzle state space
  utils/
    heap.py         ← generic min-heap priority queue
    display.py      ← terminal rendering (colorama)
  levels/
    puzzles.json    ← 14 verified real puzzles (5×5 to 9×9)
```

## Related

[../maze-pathfinding/](../maze-pathfinding/) — A\* on spatial grids,
the simpler case that motivates this abstract state-space version.
