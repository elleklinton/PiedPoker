from typing import Dict

from hands.base_hand import BaseHand
from hands.high_card import HighCard
from hands.one_pair import OnePair
from hands.poker_hand import PokerHand
from hands.two_pair import TwoPair


class LookupTableHands:
    HAND_TYPE_TO_I: Dict[BaseHand.__class__, int] = {}

    I_TO_HAND_TYPE: Dict[int, BaseHand.__class__] = {}

    @staticmethod
    def maybe_initialize():
        if not LookupTableHands.HAND_TYPE_TO_I:
            for hand in PokerHand.ALL_HANDS_RANKED:
                LookupTableHands.HAND_TYPE_TO_I[hand] = hand.hand_rank
                LookupTableHands.I_TO_HAND_TYPE[hand.hand_rank] = hand

    @staticmethod
    def i_to_hand_type(i: int):
        LookupTableHands.maybe_initialize()
        return LookupTableHands.I_TO_HAND_TYPE[i]

    @staticmethod
    def hand_type_to_i(hand_type: BaseHand.__class__):
        LookupTableHands.maybe_initialize()
        return LookupTableHands.HAND_TYPE_TO_I[hand_type]


