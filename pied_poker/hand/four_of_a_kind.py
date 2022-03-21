from typing import List

from pied_poker.card.card import Card
from pied_poker.hand import BaseHand


class FourOfAKind(BaseHand):
    hand_rank = 7

    def __init__(self, cards: List[Card]):
        """
        It is assumed that this hand has nothing higher than four of a kind
        :param cards:
        :type cards:
        """
        raise NotImplementedError('Error: You cannot initialize this class directly. You must call BaseHand.asHand()')

    @property
    def is_hand(self):
        return len(self.ranks_quad) >= 1

    @property
    def cards_in_hand(self):
        return [c for c in self.cards_sorted if c.rank in self.ranks_quad][:4]

    @property
    def cards_not_in_hand(self):
        return [c for c in self.cards_sorted if c.rank not in self.ranks_quad][:1]

    def __eq__(self, other):
        if super().__eq__(other):  # Same class of hand
            return self.ranks_quad[0] == other.ranks_quad[0] and self.cards_not_in_hand == other.cards_not_in_hand
        return False

    def __gt__(self, other):
        if super().__gt__(other):
            return True
        elif super().__lt__(other):
            return False
        else:
            if self.ranks_quad[0] > other.ranks_quad[0]:
                return True
            elif self.ranks_quad[0] < other.ranks_quad[0]:
                return False
            else:
                if not self.cards_not_in_hand or not other.cards_not_in_hand:
                    return False
                return self.cards_not_in_hand[0] > other.cards_not_in_hand[0]

    def __lt__(self, other):
        if super().__gt__(other):
            return False
        elif super().__lt__(other):
            return True
        else:
            if self.ranks_quad[0] < other.ranks_quad[0]:
                return True
            elif self.ranks_quad[0] > other.ranks_quad[0]:
                return False
            else:
                if not self.cards_not_in_hand or not other.cards_not_in_hand:
                    return False
                return self.cards_not_in_hand[0] < other.cards_not_in_hand[0]

    def __hash__(self):
        return hash(str(self))
