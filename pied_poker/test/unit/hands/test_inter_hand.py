import unittest

from pied_poker.hand import BaseHand
from pied_poker.hand.flush import Flush
from pied_poker.hand import FourOfAKind
from pied_poker.hand import FullHouse
from pied_poker.hand import HighCard
from pied_poker.hand import OnePair
from pied_poker.hand import RoyalFlush
from pied_poker.hand import Straight
from pied_poker.hand import StraightFlush
from pied_poker.hand import ThreeOfAKind
from pied_poker.hand import TwoPair
from pied_poker.test.unit.hands.hand_test_utils import HandTestUtils

ALL_RANKED_HANDS = [
    BaseHand(HandTestUtils.build_shorthand('10d', 'jd', 'qd', 'kd', 'ad')).as_hand(RoyalFlush),
    BaseHand(HandTestUtils.build_shorthand('9d', '10d', 'jd', 'qd', 'kd')).as_hand(StraightFlush),
    BaseHand(HandTestUtils.build_shorthand('9d', '9c', '9h', '9s', 'kd')).as_hand(FourOfAKind),
    BaseHand(HandTestUtils.build_shorthand('9d', '9c', 'jd', 'js', 'jh')).as_hand(FullHouse),
    BaseHand(HandTestUtils.build_shorthand('2d', '4d', '8d', 'qd', 'kd')).as_hand(Flush),
    BaseHand(HandTestUtils.build_shorthand('9d', '10h', 'js', 'qc', 'kd')).as_hand(Straight),
    BaseHand(HandTestUtils.build_shorthand('9d', '9c', '9h', 'qd', 'kd')).as_hand(ThreeOfAKind),
    BaseHand(HandTestUtils.build_shorthand('9d', '9h', '10d', '10h', 'kd')).as_hand(TwoPair),
    BaseHand(HandTestUtils.build_shorthand('9d', '9h', 'jd', 'qd', 'kd')).as_hand(OnePair),
    BaseHand(HandTestUtils.build_shorthand('9d', '2c', '6h', 'qd', 'as')).as_hand(HighCard),
]


class TestInterHand(unittest.TestCase):
    def test_all_hand_combos(self):
        for i_hand_one in range(len(ALL_RANKED_HANDS)):
            for i_hand_two in range(len(ALL_RANKED_HANDS)):
                hand_one = ALL_RANKED_HANDS[i_hand_one]
                hand_two = ALL_RANKED_HANDS[i_hand_two]

                self.assertTrue(hand_one.is_hand, 'Test failure: expected hand_one to be hand of class')
                self.assertTrue(hand_two.is_hand, 'Test failure: expected hand_two to be hand of class')

                if i_hand_one < i_hand_two:
                    self.assertNotEqual(hand_one, hand_two)
                    self.assertGreater(hand_one, hand_two)
                    self.assertFalse(hand_one < hand_two, f'Test Failed:\n{hand_one}\n<\n{hand_two}\n(expected gt)')
                elif i_hand_one == i_hand_two:
                    self.assertEqual(hand_one, hand_two)
                    self.assertFalse(hand_one > hand_two, f'Test Failed:\n{hand_one}\n!>\n{hand_two}\n(expected eq)')
                    self.assertFalse(hand_one < hand_two, f'Test Failed:\n{hand_one}\n<\n{hand_two}\n(expected eq)')
                elif i_hand_one > i_hand_two:
                    self.assertNotEqual(hand_one, hand_two)
                    self.assertFalse(hand_one > hand_two, f'Test Failed:\n{hand_one}\n!>\n{hand_two}\n(expected lt)')
                    self.assertLess(hand_one, hand_two)

    def test_hashes_unique(self):
        s = set(ALL_RANKED_HANDS)
        assert len(s) == len(ALL_RANKED_HANDS)


