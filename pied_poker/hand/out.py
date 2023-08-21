from typing import List

from pied_poker.hand.base_hand import BaseHand
from pied_poker.card.card import Card


class Out:
    def __init__(self, out_class: BaseHand.__class__, cards: List[Card]):
        """
        Used to track outs available to players
        :param out_class: The class of the out
        :type out_class: BaseHand.__class__
        :param cards: The cards that would give the player the out
        :type cards: List[Card]
        """
        self.out_class = out_class
        self.cards = cards

    def __eq__(self, other):
        return self.out_class == other.out_class and self.cards == other.cards

    def __str__(self):
        return f'Out({self.out_class.__name__}, {self.cards})'

    def __repr__(self):
        return str(self)
