from typing import List, Set

from pied_poker.card.suit import Suit
from pied_poker.card.card import Card
from pied_poker.hand import BaseHand
from pied_poker.hand import HighCard


class ThreeOfAKind(BaseHand):
    hand_rank = 3

    def __init__(self, cards: List[Card]):
        """
        It is assumed that this hand has nothing higher than three of a kind
        :param cards:
        :type cards:
        """
        raise NotImplementedError('Error: You cannot initialize this class directly. You must call BaseHand.asHand()')

    @property
    def is_hand(self):
        return len(self.ranks_triple) >= 1

    @property
    def cards_in_hand(self):
        return [c for c in self.cards_sorted if c.rank in self.ranks_triple]

    @property
    def cards_not_in_hand(self):
        return [c for c in self.cards_sorted if c.rank not in self.ranks_triple][:2]

    def __eq__(self, other):
        if super().__eq__(other):  # Same class of hand
            if self.ranks_triple[0] == other.ranks_triple[0]:  # Same triple
                # If have same triple, we delegate to HighCard to determine the winner on the rest of the cards at stake
                return BaseHand(self.cards_not_in_hand).as_hand(HighCard) == BaseHand(other.cards_not_in_hand).as_hand(HighCard)
        return False

    def __gt__(self, other):
        if super().__gt__(other):
            return True
        elif super().__lt__(other):
            return False
        else:
            if self.ranks_triple[0] > other.ranks_triple[0]:
                return True
            elif self.ranks_triple[0] < other.ranks_triple[0]:
                return False
            else:  # Same trip card_internals, delegate to HighCard to determine winner
                return BaseHand(self.cards_not_in_hand).as_hand(HighCard) > BaseHand(other.cards_not_in_hand).as_hand(HighCard)

    def __lt__(self, other):
        if super().__gt__(other):
            return False
        if super().__lt__(other):
            return True
        else:
            if self.ranks_triple[0] < other.ranks_triple[0]:
                return True
            elif self.ranks_triple[0] > other.ranks_triple[0]:
                return False
            else:  # Same trip card_internals, delegate to HighCard to determine winner
                return BaseHand(self.cards_not_in_hand).as_hand(HighCard) < BaseHand(other.cards_not_in_hand).as_hand(HighCard)

    def __hash__(self):
        return hash(str(self))

    def __hand_outs__(self, out_cards: Set[Card]) -> List[Card]:
        rv = []
        for c in self.ranks_pair:
            for s in Suit.ALLOWED_VALUES:
                card = Card(c.value, s)
                if card not in self.cards_set and card not in out_cards:
                    rv.append(card)
                    out_cards.update([card])
        return rv



