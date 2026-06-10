import argparse
import json
import random
import time
from pathlib import Path

from puzzle.board import Board, Position, ColorPair
from puzzle.state import PuzzleState
from puzzle import solver
from utils import display


PUZZLES_FILE = Path(__file__).parent / "levels" / "puzzles.json"


def load_board(data: dict) -> Board:
    colors = [
        ColorPair(
            name=name,
            start=Position(endpoints[0][0], endpoints[0][1]),
            end=Position(endpoints[1][0], endpoints[1][1]),
        )
        for name, endpoints in data["colors"].items()
    ]
    return Board(data["size"], colors)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Color Flow — A* solver")
    parser.add_argument("--index", type=int, default=None,
                        help="Puzzle index (default: random)")
    parser.add_argument("--size", type=int, default=None,
                        help="Filter by grid size")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    with open(PUZZLES_FILE) as f:
        data = json.load(f)

    puzzles = data["puzzles"]

    if args.size:
        puzzles = [p for p in puzzles if p["size"] == args.size]
        if not puzzles:
            print(f"  No puzzles found for size {args.size}.")
            return

    puzzle_data = puzzles[args.index] if args.index is not None else random.choice(puzzles)

    board = load_board(puzzle_data)
    initial = PuzzleState.initial(board)

    display.show_welcome()
    display.show_puzzle(board, initial)

    input("\n  Press Enter to solve...")

    start_time = time.time()
    solution = solver.solve(initial)
    elapsed = time.time() - start_time

    print()
    if solution:
        display.show_solution(board, solution)
        display.show_stats(elapsed, board.size, len(board.colors))
    else:
        display.show_no_solution()


if __name__ == "__main__":
    main()
