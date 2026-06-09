from enum import Enum
from game.hand import Hand


DEALER_STAND_VALUE = 17


class Outcome(Enum):
    PLAYER_BLACKJACK = "Blackjack! You win 1.5x!"
    PLAYER_WIN = "You win!"
    DEALER_WIN = "Dealer wins."
    PUSH = "Push — it's a tie."
    PLAYER_BUST = "Bust! You lose."
    DEALER_BUST = "Dealer busts! You win!"


def determine_outcome(player: Hand, dealer: Hand) -> Outcome:
    if player.is_bust():
        return Outcome.PLAYER_BUST
    if dealer.is_bust():
        return Outcome.DEALER_BUST
    if player.is_blackjack() and not dealer.is_blackjack():
        return Outcome.PLAYER_BLACKJACK
    if dealer.is_blackjack() and not player.is_blackjack():
        return Outcome.DEALER_WIN

    player_val = player.value()
    dealer_val = dealer.value()

    if player_val > dealer_val:
        return Outcome.PLAYER_WIN
    if dealer_val > player_val:
        return Outcome.DEALER_WIN
    return Outcome.PUSH


def payout(outcome: Outcome, bet: int) -> int:
    if outcome == Outcome.PLAYER_BLACKJACK:
        return int(bet * 1.5)
    if outcome in (Outcome.PLAYER_WIN, Outcome.DEALER_BUST):
        return bet
    if outcome == Outcome.PUSH:
        return 0
    return -bet


