import os
import time
from colorama import init, Fore, Back, Style
from maze.grid import Grid, Position, CellType

init(autoreset=True)

PATH            = "  "
ANIMATION_DELAY = 0.012


def _clear() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def _render(
    grid: Grid,
    open_set: set[Position],
    closed_set: set[Position],
    path_set: set[Position],
) -> str:
    rows = []
    for r in range(grid.rows):
        row = ""
        for c in range(grid.cols):
            pos  = Position(r, c)
            cell = grid.get(pos)

            if cell == CellType.WALL:
                row += Back.WHITE + Style.DIM + "  " + Style.RESET_ALL
            elif cell == CellType.START:
                row += Back.CYAN + Fore.BLACK + Style.BRIGHT + " S" + Style.RESET_ALL
            elif cell == CellType.END:
                row += Back.MAGENTA + Fore.WHITE + Style.BRIGHT + " E" + Style.RESET_ALL
            elif pos in path_set:
                row += Back.GREEN + "  " + Style.RESET_ALL
            elif pos in closed_set:
                row += Back.RED + "  " + Style.RESET_ALL
            elif pos in open_set:
                row += Back.YELLOW + "  " + Style.RESET_ALL
            else:
                row += PATH

        rows.append(row)
    return "\n".join(rows)


def _legend() -> str:
    return (
        f"\n  {Back.YELLOW}  {Style.RESET_ALL} open   "
        f"{Back.RED}  {Style.RESET_ALL} closed   "
        f"{Back.GREEN}  {Style.RESET_ALL} path\n"
    )


def animate_solving(
    grid: Grid,
    events: list[tuple[str, Position]],
    path: list[Position] | None,
) -> None:
    open_set:   set[Position] = set()
    closed_set: set[Position] = set()

    for event, pos in events:
        if event == "open":
            open_set.add(pos)
        elif event == "close":
            open_set.discard(pos)
            closed_set.add(pos)

        _clear()
        print(_render(grid, open_set, closed_set, set()))
        print(_legend())
        time.sleep(ANIMATION_DELAY)

    if path:
        path_set = set(path)
        _clear()
        print(_render(grid, set(), closed_set, path_set))
        print(_legend())
        print(
            f"  Path length: {Fore.GREEN}{len(path)}{Style.RESET_ALL} steps  |  "
            f"Cells explored: {Fore.RED}{len(closed_set)}{Style.RESET_ALL}"
        )
    else:
        print("\n  No path found.")


def show_maze(grid: Grid) -> None:
    print(_render(grid, set(), set(), set()))


def show_welcome() -> None:
    print(Fore.CYAN + Style.BRIGHT + "=" * 42 + Style.RESET_ALL)
    print(Fore.CYAN + Style.BRIGHT + "       MAZE PATHFINDING — A*" + Style.RESET_ALL)
    print(Fore.CYAN + Style.BRIGHT + "=" * 42 + Style.RESET_ALL)
