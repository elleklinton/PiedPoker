from typing import List

from pied_poker.hand.base_hand import BaseHand
from pied_poker.card.card import Card


class KillerCard:
    def __init__(self, killer_hand_class: BaseHand.__class__, cards: List[Card]):
        """
        Used to track killer cards available to players
        :param killer_hand_class: The class of the out
        :type killer_hand_class: BaseHand.__class__
        :param cards: The cards that would give the player the out
        :type cards: List[Card]
        """
        self.killer_hand_class = killer_hand_class
        self.cards = cards

    def __eq__(self, other):
        return self.killer_hand_class == other.killer_hand_class and self.cards == other.cards

    def __str__(self):
        return f'KillerCard({self.killer_hand_class.__name__}, {self.cards})'

    def __repr__(self):
        return str(self)
