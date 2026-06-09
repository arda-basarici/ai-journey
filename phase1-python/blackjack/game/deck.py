import random
from game.card import Card, Rank, Suit


class Deck:
    def __init__(self):
        self._cards: list[Card] = [
            Card(rank, suit)
            for suit in Suit
            for rank in Rank
        ]
        self.shuffle()

    def shuffle(self) -> None:
        random.shuffle(self._cards)

    def deal(self) -> Card:
        if not self._cards:
            raise ValueError("Deck is empty")
        return self._cards.pop()

    def cards_remaining(self) -> int:
        return len(self._cards)
