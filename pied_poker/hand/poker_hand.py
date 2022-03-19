from typing import List

from pied_poker.card.card import Card
from pied_poker.hand.flush import Flush
from pied_poker.hand.four_of_a_kind import FourOfAKind
from pied_poker.hand.full_house import FullHouse
from pied_poker.hand.high_card import HighCard
from pied_poker.hand.one_pair import OnePair
from pied_poker.hand.royal_flush import RoyalFlush
from pied_poker.hand.straight import Straight
from pied_poker.hand.straight_flush import StraightFlush
from pied_poker.hand.three_of_a_kind import ThreeOfAKind
from pied_poker.hand.two_pair import TwoPair
from pied_poker.hand.base_hand import BaseHand


class PokerHand(BaseHand):
    ALL_HANDS_RANKED = [
        RoyalFlush,
        StraightFlush,
        FourOfAKind,
        FullHouse,
        Flush,
        Straight,
        ThreeOfAKind,
        TwoPair,
        OnePair,
        HighCard
    ]

    def __init__(self, cards: List[Card]):
        """A class used to represent a hand of cards in poker.

        Used to compare different hands to find the greater hand.
        Example:
        cards = [Card('ah'), Card('ad'), Card('as'), Card('kh'), Card('kd')]
        hand = PokerHand(cards)
        hand.as_best_hand() # Converts the hand to a FullHouse hand type since that's the best hand
        hand.is_hand # returns True because the hand is a full house

        :param cards: Cards in the hand
        :type cards: List[Card]
        """
        super().__init__(cards)

    def as_hand(self, target_class):
        """
        Converts this generic hand to a specific class of hand
        :param target_class:
        :type target_class:
        :return:
        :rtype:
        """
        return super().as_hand(target_class)

    def as_best_hand(self):
        for hand_class in self.ALL_HANDS_RANKED:
            self.as_hand(hand_class)
            if self.is_hand:  # This will always be true for HighCard, so this will always be reached
                return self

    def __hash__(self):
        return super(PokerHand, self).__hash__()
