from typing import List

from card_internals.card import Card
from hands.base_hand import BaseHand


class PokerHandFromTable:
    def __init__(self, cards: List[Card], hand_type: BaseHand.__class__, cards_rank: int):
        self.cards_sorted = cards
        self.hand_type = hand_type
        self.hand_rank = hand_type.hand_rank
        self.cards_rank = cards_rank

    def __eq__(self, other):
        return self.hand_rank == other.hand_rank and self.cards_rank == other.cards_rank

    def __gt__(self, other):
        if self.hand_rank > other.hand_rank:
            return True
        elif self.hand_rank == other.hand_rank:
            return self.cards_rank > other.cards_rank
        return False

    def __lt__(self, other):
        if self.hand_rank < other.hand_rank:
            return True
        elif self.hand_rank == other.hand_rank:
            return self.cards_rank < other.cards_rank
        return False
