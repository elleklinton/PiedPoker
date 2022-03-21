from typing import List

from pied_poker.card.card import Card
from pied_poker.hand import BaseHand


class Straight(BaseHand):
    hand_rank = 4

    def __init__(self, cards: List[Card]):
        """
        It is assumed that this hand has nothing higher than a straight
        :param cards:
        :type cards:
        """
        raise NotImplementedError('Error: You cannot initialize this class directly. You must call BaseHand.asHand()')

    @property
    def is_hand(self):
        return bool(self.top_straight)

    @property
    def cards_in_hand(self):
        return self.top_straight if self.top_straight else []

    @property
    def cards_not_in_hand(self):
        return [] if self.top_straight else self.cards_sorted[:5]

    def __eq__(self, other):
        if super().__eq__(other):  # Same class of hand
            return self.top_straight[0] == other.top_straight[0]
        return False

    def __gt__(self, other):
        if super().__gt__(other):
            return True
        elif super().__lt__(other):
            return False
        else:
            return self.top_straight[0] > other.top_straight[0]

    def __lt__(self, other):
        if super().__gt__(other):
            return False
        if super().__lt__(other):
            return True
        else:
            return self.top_straight[0] < other.top_straight[0]

    def __hash__(self):
        return hash(str(self))



