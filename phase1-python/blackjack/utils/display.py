from game.hand import Hand
from game.rules import Outcome


DIVIDER = "-" * 40


def clear_line() -> None:
    print()


def show_divider() -> None:
    print(DIVIDER)


def show_welcome() -> None:
    print(DIVIDER)
    print("        BLACKJACK")
    print(DIVIDER)


def show_balance(balance: int) -> None:
    print(f"Balance: ${balance}")


def show_bet(bet: int) -> None:
    print(f"Bet: ${bet}")


def show_dealer_hand(hand: Hand, hide_second: bool = False) -> None:
    if hide_second and len(hand.cards) >= 2:
        visible = str(hand.cards[0])
        print(f"Dealer: {visible}  [hidden]")
    else:
        print(f"Dealer: {hand}  (value: {hand.value()})")


def show_player_hand(hand: Hand) -> None:
    print(f"You:    {hand}  (value: {hand.value()})")

def show_player_blackjack() -> None:
    print("Congratulations! You got a Blackjack!")


def show_outcome(outcome: Outcome, balance_change: int) -> None:
    print(DIVIDER)
    symbol = "+" if balance_change >= 0 else ""
    print(f"  {outcome.value}  ({symbol}${balance_change})")
    print(DIVIDER)


def prompt_bet(balance: int) -> int:
    while True:
        try:
            bet = int(input(f"Place your bet (1-{balance}): $"))
            if 1 <= bet <= balance:
                return bet
            print(f"Bet must be between $1 and ${balance}.")
        except ValueError:
            print("Please enter a valid number.")


def prompt_action() -> str:
    while True:
        action = input("Action — [h]it / [s]tand: ").strip().lower()
        if action in ("h", "hit", "s", "stand"):
            return "hit" if action in ("h", "hit") else "stand"
        print("Please enter 'h' to hit or 's' to stand.")


def prompt_play_again() -> bool:
    answer = input("Play again? [y/n]: ").strip().lower()
    return answer in ("y", "yes")


def show_game_over(balance: int) -> None:
    print(DIVIDER)
    print(f"Game over. Final balance: ${balance}")
    print(DIVIDER)
