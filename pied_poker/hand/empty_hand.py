from typing import List, Set

from pied_poker.deck.deck import Deck
from pied_poker.card.card import Card
from pied_poker.hand import BaseHand


class EmptyHand(BaseHand):
    hand_rank = -1

    def __init__(self, cards: List[Card]):
        """
        When this hand is initialized, it is assumed that all parent hands have been exhausted and are not present in the cards provided
        :param cards:
        :type cards:
        """
        raise NotImplementedError('Error: You cannot initialize this class directly. You must call BaseHand.asHand()')

    @property
    def cards_in_hand(self):
        return []

    @property
    def cards_not_in_hand(self):
        return []

    def __eq__(self, other):
        return other.hand_rank == self.hand_rank

    def __gt__(self, other):
        return other.hand_rank > self.hand_rank

    def __lt__(self, other):
        return other.hand_rank < self.hand_rank

    def __hash__(self):
        return hash(str(self))

    def __hand_outs__(self, out_cards: Set[Card]) -> List[Card]:
        return []
