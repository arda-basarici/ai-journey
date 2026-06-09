from game.deck import Deck
from game.hand import Hand
from game.rules import determine_outcome, payout, DEALER_STAND_VALUE, Outcome
from utils import display


STARTING_BALANCE = 500


class Game:
    def __init__(self):
        self.balance: int = STARTING_BALANCE
        self.deck: Deck = Deck()
        self.player_hand: Hand = Hand()
        self.dealer_hand: Hand = Hand()

    def _refresh_deck_if_needed(self) -> None:
        if self.deck.cards_remaining() < 15:
            self.deck = Deck()

    def _deal_initial_cards(self) -> None:
        self.player_hand.clear()
        self.dealer_hand.clear()
        self.player_hand.add_card(self.deck.deal())
        self.dealer_hand.add_card(self.deck.deal())
        self.player_hand.add_card(self.deck.deal())
        self.dealer_hand.add_card(self.deck.deal())

    def _player_turn(self) -> None:
        while True:
            display.clear_line()
            display.show_dealer_hand(self.dealer_hand, hide_second=True)
            display.show_player_hand(self.player_hand)

            if self.player_hand.is_bust():
                break
            if self.player_hand.is_blackjack():
                display.show_player_blackjack()
                break

            action = display.prompt_action()
            if action == "stand":
                break
            self.player_hand.add_card(self.deck.deal())

    def _dealer_turn(self) -> None:
        while self.dealer_hand.value() < DEALER_STAND_VALUE:
            self.dealer_hand.add_card(self.deck.deal())

    def play_round(self) -> bool:
        self._refresh_deck_if_needed()

        display.show_divider()
        display.show_balance(self.balance)

        bet = display.prompt_bet(self.balance)

        self._deal_initial_cards()

        self._player_turn()

        if not self.player_hand.is_bust():
            self._dealer_turn()

        outcome = determine_outcome(self.player_hand, self.dealer_hand)
        change = payout(outcome, bet)
        self.balance += change

        display.clear_line()
        display.show_dealer_hand(self.dealer_hand)
        display.show_player_hand(self.player_hand)
        display.show_outcome(outcome, change)
        display.show_balance(self.balance)

        if self.balance <= 0:
            return False

        return display.prompt_play_again()

    def run(self) -> None:
        display.show_welcome()

        playing = True
        while playing:
            playing = self.play_round()

        display.show_game_over(self.balance)
