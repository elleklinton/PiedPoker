from typing import List, Set, Generic

from pied_poker.card.card import Card
from pied_poker.hand import BaseHand, Flush


class StraightFlush(BaseHand):
    hand_rank = 8

    def __init__(self, cards: List[Card]):
        """
        It is assumed that this hand has nothing higher than straight flush
        :param cards:
        :type cards:
        """
        raise NotImplementedError('Error: You cannot initialize this class directly. You must call BaseHand.asHand()')

    @property
    def is_hand(self):
        return bool(self.straight_flush)

    @property
    def cards_in_hand(self):
        return self.straight_flush

    @property
    def cards_not_in_hand(self):
        return []

    def __eq__(self, other):
        if super().__eq__(other):  # Same class of hand
            return self.straight_flush[0] == other.straight_flush[0]
        return False

    def __gt__(self, other):
        if super().__gt__(other):
            return True
        elif super().__lt__(other):
            return False
        else:
            return self.straight_flush[0] > other.straight_flush[0]

    def __lt__(self, other):
        if super().__gt__(other):
            return False
        if super().__lt__(other):
            return True
        else:
            return self.straight_flush[0] < other.straight_flush[0]

    def __hash__(self):
        return hash(str(self))

    def __hand_outs__(self, out_cards: Set[Card], include_higher_hand_outs=False) -> List[Card]:
        rv = []
        for flushOut in self.as_hand(Flush).__hand_outs__({*out_cards}, True):
            newHand = BaseHand(self.cards_sorted + [flushOut]).as_hand(StraightFlush)
            if newHand.is_hand and flushOut not in out_cards:
                if newHand.__class__.hand_rank == StraightFlush.hand_rank or \
                        (newHand.hand_rank > self.hand_rank and include_higher_hand_outs):
                    rv.append(flushOut)
                    out_cards.update([flushOut])
        return rv
