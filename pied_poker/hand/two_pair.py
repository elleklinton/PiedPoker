from typing import List, Set

from pied_poker.card.suit import Suit
from pied_poker.card.card import Card
from pied_poker.hand import BaseHand


class TwoPair(BaseHand):
    hand_rank = 2

    def __init__(self, cards: List[Card]):
        """
        It is assumed that this hand has nothing higher than two pair
        :param cards:
        :type cards:
        """
        raise NotImplementedError('Error: You cannot initialize this class directly. You must call BaseHand.asHand()')

    @property
    def is_hand(self):
        return len(self.ranks_pair) >= 2

    @property
    def cards_in_hand(self):
        return [c for c in self.cards_sorted if c.rank in self.ranks_pair]

    @property
    def cards_not_in_hand(self):
        # Only take the first high card_internals since 2 pair takes up 4/5 cards
        return [c for c in self.cards_sorted if c.rank not in self.ranks_pair][:1]

    def __eq__(self, other):
        if super().__eq__(other):  # Same class of hand
            if self.ranks_pair[0] == other.ranks_pair[0]:  # Same top pair
                if self.ranks_pair[1] == other.ranks_pair[1]: # Same bottom pair
                    # Only equal if same kicker card_internals
                    return self.cards_not_in_hand == other.cards_not_in_hand
        return False

    def __gt__(self, other):
        if super().__gt__(other):
            return True
        elif super().__lt__(other):
            return False
        else:
            if self.ranks_pair[0] > other.ranks_pair[0]:
                return True
            elif self.ranks_pair[0] < other.ranks_pair[0]:
                return False
            else:  # Same top pair
                if self.ranks_pair[1] > other.ranks_pair[1]:
                    return True
                elif self.ranks_pair[1] < other.ranks_pair[1]:
                    return False
                else:  # Same top and bottom pair, comes down to kicker card_internals
                    if not self.cards_not_in_hand or not other.cards_not_in_hand:
                        return False
                    return self.cards_not_in_hand[0] > other.cards_not_in_hand[0]

    def __lt__(self, other):
        if super().__gt__(other):
            return False
        elif super().__lt__(other):
            return True
        else:
            if self.ranks_pair[0] < other.ranks_pair[0]:
                return True
            elif self.ranks_pair[0] > other.ranks_pair[0]:
                return False
            else:  # Same top pair
                if self.ranks_pair[1] < other.ranks_pair[1]:
                    return True
                elif self.ranks_pair[1] > other.ranks_pair[1]:
                    return False
                else:  # Same top and bottom pair, comes down to kicker card_internals
                    if not self.cards_not_in_hand or not other.cards_not_in_hand:
                        return False
                    return self.cards_not_in_hand[0] < other.cards_not_in_hand[0]

    def __hash__(self):
        return hash(str(self))

    def __hand_outs__(self, out_cards: Set[Card]) -> List[Card]:
        rv = []
        if len(self.ranks_pair) == 1:
            for r in self.ranks_single:
                for s in Suit.ALLOWED_VALUES:
                    card = Card(r.value, s)
                    if card not in self.cards_set and card not in out_cards:
                        rv.append(card)
                        out_cards.update([card])
        return rv





