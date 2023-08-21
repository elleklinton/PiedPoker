from typing import List, Set
from itertools import combinations

from pied_poker.card.suit import Suit
from pied_poker.card.rank import Rank
from pied_poker.card.card import Card
from pied_poker.hand.base_hand import BaseHand


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
        # TODO bug: NEed to check if double or triple rank is higher in case both are present i.e. AAA KKK QQ would select wrong hand
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

    def __hand_outs__(self, out_cards: Set[Card]) -> List[Card]:
        rv = []

        rank_outs: List[Rank] = []

        # Two cases to make full house: either 2 pair, or one triple with 1 single
        if len(self.ranks_pair) >= 2:
            # In this case, we already have 2 pair,
            # so need to iterate over each pair we have and get the remaining suits
            rank_outs = self.ranks_pair
        elif len(self.ranks_triple) >= 1 and len(self.ranks_single) >= 1:
            # TODO: possible bug -- could maybe be both of these cases, not one or the other
            # In this case, we already have a triple.
            # So a pair with any of the ranks_single will complete the full house
            rank_outs = self.ranks_single

        for r in rank_outs:
            for s in Suit.ALLOWED_VALUES:
                card = Card(r.value, s)
                if card not in self.cards_set and card not in out_cards:
                    rv.append(card)
                    out_cards.update([card])

        return rv
