from typing import List

from card_internals.card import Card
from hands.flush import Flush
from hands.four_of_a_kind import FourOfAKind
from hands.full_house import FullHouse
from hands.high_card import HighCard
from hands.one_pair import OnePair
from hands.royal_flush import RoyalFlush
from hands.straight import Straight
from hands.straight_flush import StraightFlush
from hands.three_of_a_kind import ThreeOfAKind
from hands.two_pair import TwoPair
from hands.base_hand import BaseHand


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

    @staticmethod
    def rank_to_hand_class(hand_rank: int):
        return PokerHand.ALL_HANDS_RANKED[len(PokerHand.ALL_HANDS_RANKED) - hand_rank - 1]
