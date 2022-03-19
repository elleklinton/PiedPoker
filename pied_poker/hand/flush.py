from typing import List

from pied_poker.card.card import Card
from pied_poker.hand.base_hand import BaseHand


class Flush(BaseHand):
    hand_rank = 5

    def __init__(self, cards: List[Card]):
        """
        It is assumed that this hand has nothing higher than a flush
        :param cards:
        :type cards:
        """
        raise NotImplementedError('Error: You cannot initialize this class directly. You must call BaseHand.asHand()')

    @property
    def is_hand(self):
        return bool(self.flush_suit)

    @property
    def cards_in_hand(self):
        return [c for c in self.cards_sorted if c.suit == self.flush_suit][:5]

    @property
    def cards_not_in_hand(self):
        return []

    def __eq__(self, other):
        if super().__eq__(other):  # Same class of hand
            return self.cards_in_hand[0] == other.cards_in_hand[0]
        return False

    def __gt__(self, other):
        if super().__gt__(other):
            return True
        elif super().__lt__(other):
            return False
        else:
            return self.cards_in_hand[0] > other.cards_in_hand[0]

    def __lt__(self, other):
        if super().__gt__(other):
            return False
        if super().__lt__(other):
            return True
        else:
            return self.cards_in_hand[0] < other.cards_in_hand[0]

    def __hash__(self):
        return hash(str(self))




