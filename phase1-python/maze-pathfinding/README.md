# Maze Pathfinding — A\*

Procedurally generated mazes solved with A\*, with real-time animated
terminal visualization of the search process.

## How it works

### Maze generation — Recursive Backtracker

Carves paths through an all-wall grid using iterative DFS with random
neighbor selection. Every generated maze is guaranteed to have a solution.
After generation, a configurable fraction of interior walls are removed
to add loops and alternate routes — making the A\* search more visually
interesting and the maze more challenging.

### Pathfinding — A\*

Explores cells ordered by `f(n) = g(n) + h(n)`:

- `g(n)` — actual steps taken from start
- `h(n)` — Manhattan distance estimate to end

The animation shows the algorithm's internal state in real time:

- 🟡 **Yellow** — open set (frontier, queued to explore)
- 🔴 **Red** — closed set (already processed)
- 🟢 **Green** — final shortest path

## Usage

```bash
pip install -r requirements.txt
python main.py
```

Optional arguments:

```bash
python main.py --rows 41 --cols 41 --loop-factor 0.20
```

| Argument        | Default | Description                         |
| --------------- | ------- | ----------------------------------- |
| `--rows`        | 41      | Maze height (auto-corrected to odd) |
| `--cols`        | 41      | Maze width (auto-corrected to odd)  |
| `--loop-factor` | 0.17    | Extra wall removal 0.0–0.3          |

## Project structure

```
maze-pathfinding/
  main.py              ← entry point, argument parsing
  maze/
    grid.py            ← Grid, Position, CellType
    generator.py       ← iterative Recursive Backtracker + loop injection
    solver.py          ← A* with open/close set callbacks
  utils/
    heap.py            ← generic min-heap (heapq wrapper)
    display.py         ← terminal rendering and animation (colorama)
```

## Design notes

**Solver decoupled from display via callbacks**

```python
solver.solve(grid, start, end, on_open=..., on_close=...)
```

The solver fires `on_open` when a cell enters the frontier and `on_close`
when it's processed. `main.py` collects these as typed events and passes
them to the animator. The solver has no knowledge of how it is visualized.

**Iterative maze generation**

The carving algorithm uses an explicit stack instead of recursion.
Python's default recursion limit (~1000) would crash on mazes larger
than ~45x45. The iterative version handles arbitrarily large grids.

**Generic priority queue**

`PriorityQueue[T]` wraps `heapq` with a clean typed interface. A
tie-breaking counter prevents comparison errors when two nodes share
the same priority — a subtle but important correctness detail.

## Background

Previously implemented A\* in TypeScript for two different use cases:
spatial pathfinding in generated mazes, and abstract state-space search
for a color flow puzzle solver. This project is the Python reimplementation
of the spatial case.

The abstract state-space version is in [../color-puzzle/](../color-puzzle/).
