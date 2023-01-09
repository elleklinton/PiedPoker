from typing import List

from pied_poker import Rank
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
            card_i_to_compare = 0
            while card_i_to_compare < len(self.cards_in_hand):
                if self.cards_in_hand[card_i_to_compare] != other.cards_in_hand[card_i_to_compare]:
                    return False
                card_i_to_compare += 1
            return True
        return False

    def __gt__(self, other):
        if super().__gt__(other):
            return True
        elif super().__lt__(other):
            return False
        else:
            card_i_to_compare = 0
            while card_i_to_compare < len(self.cards_in_hand):
                if self.cards_in_hand[card_i_to_compare] > other.cards_in_hand[card_i_to_compare]:
                    return True
                card_i_to_compare += 1
            return False

    def __lt__(self, other):
        if super().__gt__(other):
            return False
        if super().__lt__(other):
            return True
        else:
            card_i_to_compare = 0
            while card_i_to_compare < len(self.cards_in_hand):
                if self.cards_in_hand[card_i_to_compare] < other.cards_in_hand[card_i_to_compare]:
                    return True
                card_i_to_compare += 1
            return False

    def __hash__(self):
        return hash(str(self))

    def __hand_outs__(self) -> List[Card]:
        rv = []
        for (suit, count) in self.suit_counts.items():
            if count == 4:
                for r in Rank.ALLOWED_VALUES:
                    card = Card(r, suit.value)
                    if card not in self.cards_set:
                        rv.append(card)

        return rv





