from colorama import init, Style
from puzzle.board import Board, Position
from puzzle.state import PuzzleState

init(autoreset=True)

RESET = Style.RESET_ALL


def rgb(r: int, g: int, b: int) -> str:
    return f"\033[38;2;{r};{g};{b}m"


# 10 visually distinct RGB colors — no two are similar
COLOR_RGB: dict[str, str] = {
    "red":          rgb(255, 0,   0),
    "orange":       rgb(255, 127, 0),
    "yellow":       rgb(255, 255, 0),
    "green":        rgb(0,   255, 0),
    "cyan":         rgb(0,   255, 255),
    "blue":         rgb(0,   0,   255),
    "purple_devil": rgb(139, 0,   255),
    "magenta":      rgb(255, 0,   255),
    "pink":         rgb(255, 105, 180),
    "gray":         rgb(255, 255, 255),
    # aliases — map to nearest distinct color
    "purple_crazy": rgb(139, 0,   255),
    "red_money":    rgb(255, 0,   0),
    "maroon":       rgb(180, 0,   0),
}

CELL_W = 5

H  = "─"; V  = "│"
TL = "┌"; TR = "┐"
BL = "└"; BR = "┘"
TM = "┬"; BM = "┴"
LM = "├"; RM = "┤"
MM = "┼"

BLOCK = " ███ "
EMPTY = "     "


def _dim(s: str) -> str:
    return Style.DIM + s + RESET


def _block(color: str, bright: bool = False) -> str:
    fg = COLOR_RGB.get(color, rgb(255, 255, 255))
    b = Style.BRIGHT if bright else ""
    return fg + b + BLOCK + RESET


def _top_border(size: int) -> str:
    seg = H * CELL_W
    return _dim(TL + (seg + TM) * (size - 1) + seg + TR)


def _mid_border(size: int) -> str:
    seg = H * CELL_W
    return _dim(LM + (seg + MM) * (size - 1) + seg + RM)


def _bot_border(size: int) -> str:
    seg = H * CELL_W
    return _dim(BL + (seg + BM) * (size - 1) + seg + BR)


def _render(board: Board, state: PuzzleState) -> list[str]:
    path_cells: dict[Position, str] = {}
    for name, cs in state.color_states.items():
        for pos in cs.path:
            path_cells[pos] = name

    endpoint_cells: dict[Position, str] = {}
    for pair in board.colors:
        endpoint_cells[pair.start] = pair.name
        endpoint_cells[pair.end] = pair.name

    lines = [_top_border(board.size)]

    for r in range(board.size):
        row = _dim(V)
        for c in range(board.size):
            pos = Position(r, c)
            if pos in endpoint_cells:
                row += _block(endpoint_cells[pos], bright=True)
            elif pos in path_cells:
                row += _block(path_cells[pos], bright=True)
            else:
                row += _dim(EMPTY)
            row += _dim(V)
        lines.append(row)
        if r < board.size - 1:
            lines.append(_mid_border(board.size))

    lines.append(_bot_border(board.size))
    return lines


def show_puzzle(board: Board, state: PuzzleState) -> None:
    print("\n".join(_render(board, state)))


def show_solution(board: Board, solution: PuzzleState) -> None:
    print("\n".join(_render(board, solution)))


def show_stats(elapsed: float, size: int, n_colors: int) -> None:
    print(
        f"\n  {Style.BRIGHT}{size}×{size}{RESET}  ·  "
        f"{n_colors} colors  ·  "
        f"solved in {rgb(255,255,0)}{elapsed:.3f}s{RESET}"
    )


def show_no_solution() -> None:
    print(f"\n  {rgb(255,0,0)}No solution found.{RESET}")


def show_welcome() -> None:
    print(f"\n  {Style.BRIGHT}COLOR FLOW{RESET}  ·  A* solver\n")