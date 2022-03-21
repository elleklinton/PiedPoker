from typing import List

from pied_poker.card.card import Card
from pied_poker.hand import BaseHand


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
        if len(self.ranks_triple) >= 1:
            if len(self.ranks_pair) >= 1 or len(self.ranks_triple) >= 2:
                return True
        return False

    @property
    def __trip_rank__(self):
        return self.ranks_triple[0]

    @property
    def __pair_rank__(self):
        return self.ranks_pair[0] if self.ranks_pair else self.ranks_triple[1]

    @property
    def cards_in_hand(self):
        card_ranks = {self.__trip_rank__, self.__pair_rank__}
        return [c for c in self.cards_sorted if c.rank in card_ranks][:5]

    @property
    def cards_not_in_hand(self):
        return []

    def __eq__(self, other):
        if super().__eq__(other):  # Same class of hand
            return self.__trip_rank__ == other.__trip_rank__ and self.__pair_rank__ == other.__pair_rank__
        return False

    def __gt__(self, other):
        if super().__gt__(other):
            return True
        elif super().__lt__(other):
            return False
        else:
            if self.__trip_rank__ > other.__trip_rank__:
                return True
            elif self.__trip_rank__ == other.__trip_rank__:
                return self.__pair_rank__ > other.__pair_rank__
            else:
                return False

    def __lt__(self, other):
        if super().__gt__(other):
            return False
        if super().__lt__(other):
            return True
        else:
            if self.__trip_rank__ < other.__trip_rank__:
                return True
            elif self.__trip_rank__ == other.__trip_rank__:
                return self.__pair_rank__ < other.__pair_rank__
            else:
                return False

    def __hash__(self):
        return hash(str(self))
