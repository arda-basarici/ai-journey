import argparse
from maze import generator, solver
from maze.grid import Position
from utils import display


DEFAULTS = {
    "rows": 41,
    "cols": 41,
    "loop_factor": 0.17,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Maze Pathfinding — A*")
    parser.add_argument(
        "--rows",
        type=int,
        default=DEFAULTS["rows"],
        help=f"Maze height — must be odd (default: {DEFAULTS['rows']})",
    )
    parser.add_argument(
        "--cols",
        type=int,
        default=DEFAULTS["cols"],
        help=f"Maze width — must be odd (default: {DEFAULTS['cols']})",
    )
    parser.add_argument(
        "--loop-factor",
        type=float,
        default=DEFAULTS["loop_factor"],
        help=f"Wall removal density 0.0–0.3 (default: {DEFAULTS['loop_factor']})",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    loop_factor = max(0.0, min(0.3, args.loop_factor))

    display.show_welcome()
    print(f"\n  Size: {args.rows}x{args.cols}  |  Loop factor: {loop_factor}\n")

    grid, start, end = generator.generate(args.rows, args.cols, loop_factor)

    print("Generated maze:\n")
    display.show_maze(grid)
    input("\nPress Enter to solve with A*...")

    events: list[tuple[str, Position]] = []

    path = solver.solve(
        grid, start, end,
        on_open=lambda pos: events.append(("open", pos)),
        on_close=lambda pos: events.append(("close", pos)),
    )

    display.animate_solving(grid, events, path)


if __name__ == "__main__":
    main()
