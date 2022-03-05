from typing import List

from card_internals.card import Card
from card_internals.rank import Rank
from hands.base_hand import BaseHand


class RoyalFlush(BaseHand):
    hand_rank = 9

    def __init__(self, cards: List[Card]):
        """
        It is assumed that this hand has nothing higher than royal flush
        :param cards:
        :type cards:
        """
        raise NotImplementedError('Error: You cannot initialize this class directly. You must call BaseHand.asHand()')

    @property
    def is_hand(self):
        return bool(self.straight_flush) and self.straight_flush[0].rank == Rank('a')

    @property
    def cards_in_hand(self):
        return self.straight_flush

    @property
    def cards_not_in_hand(self):
        return []

    @property
    def is_suit_dependent(self):
        return True

    def __eq__(self, other):
        if super().__eq__(other):  # Same class of hand
            return True  # All royal flushes are equal
        return False

    def __gt__(self, other):
        if super().__gt__(other):
            return True
        elif super().__lt__(other):
            return False
        else:
            return False  # All royal flushes are equal

    def __lt__(self, other):
        if super().__gt__(other):
            return False
        if super().__lt__(other):
            return True
        else:
            return False  # All royal flushes are equal

    def __hash__(self):
        return hash(str(self))


