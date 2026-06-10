from puzzle.state import PuzzleState
from utils.heap import PriorityQueue


def solve(initial: PuzzleState) -> PuzzleState | None:
    """
    A* search over the puzzle state space.

    Node:      PuzzleState — full board snapshot
    Neighbors: valid next states (one color extended by one step)
    Goal:      all colors connected, all cells filled
    Cost:      number of steps taken
    Heuristic: Manhattan distances to targets + empty cells remaining
    """
    frontier: PriorityQueue[PuzzleState] = PriorityQueue()
    frontier.push(initial, 0)

    cost_so_far: dict[int, int] = {hash(initial): 0}

    while not frontier.is_empty():
        current = frontier.pop()

        if current.is_solved():
            return current

        g = cost_so_far.get(hash(current), 0)

        for neighbor in current.next_states():
            new_g = g + 1
            h = hash(neighbor)
            if h not in cost_so_far or new_g < cost_so_far[h]:
                cost_so_far[h] = new_g
                frontier.push(neighbor, new_g + neighbor.heuristic())

    return None
