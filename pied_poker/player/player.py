from typing import List

from pied_poker.card.card import Card
from pied_poker.hand.base_hand import BaseHand


class Player:
    def __init__(self, name: str, cards: List[Card] = None, hand: BaseHand = None):
        self.name = name
        self.cards: List[Card] = cards if cards else []
        self.hand = hand

    def poker_hand(self, community_cards: List[Card]):
        self.hand = BaseHand(self.cards + community_cards)
        self.hand = self.hand.as_best_hand()
        return self.hand

    def add_community_cards(self, *cards: Card):
        for card in cards:
            self.hand.add_card(card)
        self.hand = self.hand.as_best_hand()

    def remove_community_card(self, *cards: Card):
        for card in cards:
            self.hand.remove_card(card)
        self.hand = self.hand.as_best_hand()

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        if self.hand is not None:
            return f'{self.name}: {self.hand}'
        return f'{self.name}: {self.cards}'

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return self.name.__hash__()
