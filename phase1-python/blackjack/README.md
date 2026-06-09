# Blackjack

A command-line basic Blackjack game built in Python. Single player vs dealer with full casino rules.

## What this demonstrates

- Clean class architecture with clear separation of concerns
- Enums for type-safe card representation
- Isolated display layer (all terminal output in one place)
- Type hints throughout
- Game loop design

## Rules

- Standard Blackjack: player vs dealer
- Dealer stands on 17
- Blackjack pays 1.5x
- Aces count as 11 or 1 (auto-adjusted)
- Player starts with $500

## Project structure

```
blackjack/
  main.py           ← entry point
  game/
    card.py         ← Card, Rank, Suit
    deck.py         ← Deck (shuffle, deal)
    hand.py         ← Hand (value, bust, blackjack detection)
    rules.py        ← outcome determination, payout logic
    game.py         ← Game class, round orchestration
  utils/
    display.py      ← all terminal I/O isolated here
```

## How to run

```bash
python main.py
```

No dependencies — standard library only.
