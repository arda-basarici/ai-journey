from game.card import Card, Rank


class Hand:
    def __init__(self):
        self.cards: list[Card] = []

    def add_card(self, card: Card) -> None:
        self.cards.append(card)

    def value(self) -> int:
        total = sum(card.rank.points for card in self.cards)
        aces = sum(1 for card in self.cards if card.rank.symbol == Rank.ACE)

        while total > 21 and aces:
            total -= 10
            aces -= 1

        return total

    def is_bust(self) -> bool:
        return self.value() > 21

    def is_blackjack(self) -> bool:
        return len(self.cards) == 2 and self.value() == 21

    def clear(self) -> None:
        self.cards = []

    def __str__(self) -> str:
        return "  ".join(str(card) for card in self.cards)
