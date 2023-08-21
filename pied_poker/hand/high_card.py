from typing import List, Set

from pied_poker.deck.deck import Deck
from pied_poker.card.card import Card
from pied_poker.hand import BaseHand


class HighCard(BaseHand):
    hand_rank = 0

    def __init__(self, cards: List[Card]):
        """
        When this hand is initialized, it is assumed that all parent hands have been exhausted and are not present in the cards provided
        :param cards:
        :type cards:
        """
        raise NotImplementedError('Error: You cannot initialize this class directly. You must call BaseHand.asHand()')

    def __num_to_compare__(self, other):
        return min(len(self.ranks_single), len(other.ranks_single), 5)

    @property
    def cards_in_hand(self):
        return [c for c in self.cards_sorted if c.rank in self.ranks_single][:5]

    @property
    def cards_not_in_hand(self):
        return [c for c in self.cards_sorted if c.rank in self.ranks_single][5:]

    @property
    def is_hand(self):
        return len(self.cards_sorted) > 0

    def __eq__(self, other):
        if not super().__eq__(other):
            return False
        else:  # If same type of hand, compare within the hand
            if len(self.ranks_single) != len(other.ranks_single):
                return False

            num_to_compare = self.__num_to_compare__(other) # TODO: this is not necessary as by this point the lists will be equal length
            for i in range(num_to_compare):
                if self.ranks_single[i] != other.ranks_single[i]:
                    return False
            return True

    def __gt__(self, other):
        if super().__gt__(other):
            return True
        elif super().__lt__(other):
            return False
        else:  # Same hand, compare within that hand
            if len(self.ranks_single) > len(other.ranks_single):
                return True
            elif len(self.ranks_single) < len(other.ranks_single):
                return False

            num_to_compare = self.__num_to_compare__(other)

            for i in range(num_to_compare):
                if self.ranks_single[i] < other.ranks_single[i]:
                    return False
                if self.ranks_single[i] > other.ranks_single[i]:
                    return True
            return False

    def __lt__(self, other):
        if super().__gt__(other):
            return False
        if super().__lt__(other):
            return True
        else:
            if len(self.ranks_single) > len(other.ranks_single):
                return False
            elif len(self.ranks_single) < len(other.ranks_single):
                return True

            num_to_compare = self.__num_to_compare__(other)

            for i in range(num_to_compare):
                if self.ranks_single[i] > other.ranks_single[i]:
                    return False
                if self.ranks_single[i] < other.ranks_single[i]:
                    return True
            return False

    def __hash__(self):
        return hash(str(self))

    def __hand_outs__(self, out_cards: Set[Card]) -> List[Card]:
        rv = []
        highest_curr_card = self.cards_in_hand[0] if len(self.cards_in_hand) > 0 else Deck.ALL_CARDS[0]
        for c in Deck.ALL_CARDS:
            if c > highest_curr_card and c not in out_cards:
                rv.append(c)
                out_cards.update([c])

        return rv
