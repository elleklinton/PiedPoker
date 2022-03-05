from typing import List

from card_internals.card import Card
from hands.poker_hand import PokerHand


class Player:
    def __init__(self, name: str, cards: List[Card] = None, hand: PokerHand = None):
        self.name = name
        self.cards: List[Card] = cards if cards else []
        self.hand = hand

    def poker_hand(self, community_cards: List[Card]):
        self.hand = PokerHand(self.cards + community_cards)
        self.hand = self.hand.as_best_hand()
        return self.hand

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f'{self.name}: {self.cards}'

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return self.name.__hash__()
