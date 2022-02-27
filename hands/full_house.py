from typing import List

from card_internals.card import Card
from hands.base_hand import BaseHand


class FullHouse(BaseHand):
    hand_rank = 6

    def __init__(self, cards: List[Card]):
        """
        It is assumed that this hand has nothing higher than a full house
        :param cards:
        :type cards:
        """
        raise NotImplementedError('Error: You cannot initialize this class directly. You must call BaseHand.asHand()')

    @property
    def is_hand(self):
        return len(self.ranks_pair) >= 1 and len(self.ranks_triple) >= 1

    @property
    def cards_in_hand(self):
        card_ranks = {self.ranks_pair[0], self.ranks_triple[0]}
        return [c for c in self.cards_sorted if c.rank in card_ranks][:5]

    @property
    def cards_not_in_hand(self):
        return []

    def __eq__(self, other):
        if super().__eq__(other):  # Same class of hand
            return self.ranks_triple[0] == other.ranks_triple[0] and self.ranks_pair[0] == other.ranks_pair[0]
        return False

    def __gt__(self, other):
        if super().__gt__(other):
            return True
        elif super().__lt__(other):
            return False
        else:
            if self.ranks_triple[0] > other.ranks_triple[0]:
                return True
            elif self.ranks_triple[0] == other.ranks_triple[0]:
                return self.ranks_pair[0] > other.ranks_pair[0]
            else:
                return False

    def __lt__(self, other):
        if super().__gt__(other):
            return False
        if super().__lt__(other):
            return True
        else:
            if self.ranks_triple[0] < other.ranks_triple[0]:
                return True
            elif self.ranks_triple[0] == other.ranks_triple[0]:
                return self.ranks_pair[0] < other.ranks_pair[0]
            else:
                return False

    def __hash__(self):
        return hash(str(self))
