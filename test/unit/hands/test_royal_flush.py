from unittest import TestCase

from hands.base_hand import BaseHand
from hands.royal_flush import RoyalFlush
from test.unit.hands.hand_test_utils import HandTestUtils


class FakeHigherHand(BaseHand):
    hand_rank = 10


class TestRoyalFlush(TestCase):
    def test_comparable(self):
        # Same exact royal flush
        a = HandTestUtils.build_shorthand('ad', 'kd', 'qd', 'jd', '10d')
        b = HandTestUtils.build_shorthand('ad', 'kd', 'qd', 'jd', '10d')
        HandTestUtils.assertEquals(self, RoyalFlush, a, b)

        # Same exact royal flush different suits
        a = HandTestUtils.build_shorthand('ac', 'kc', 'qc', 'jc', '10c')
        b = HandTestUtils.build_shorthand('ad', 'kd', 'qd', 'jd', '10d')
        HandTestUtils.assertEquals(self, RoyalFlush, a, b)

        # Test that fake better hand ranks higher
        a = HandTestUtils.build_shorthand('ac', 'kc', 'qc', 'jc', '10c')
        self.assertLess(BaseHand(a).as_hand(RoyalFlush), BaseHand(a).as_hand(FakeHigherHand))
        self.assertFalse(BaseHand(a).as_hand(RoyalFlush) > BaseHand(a).as_hand(FakeHigherHand))
        self.assertGreater(BaseHand(a).as_hand(FakeHigherHand), BaseHand(a).as_hand(RoyalFlush))
        self.assertFalse(BaseHand(a).as_hand(FakeHigherHand) < BaseHand(a).as_hand(RoyalFlush))

    def test_is_hand(self):
        # Test non-royal straight flush
        a = HandTestUtils.build_shorthand('kc', 'qc', 'jc', '10c', '9c')
        self.assertFalse(BaseHand(a).as_hand(RoyalFlush).is_hand)

        # Test royal non-straight flush
        a = HandTestUtils.build_shorthand('ac', 'kc', 'jc', '10c', '9c')
        self.assertFalse(BaseHand(a).as_hand(RoyalFlush).is_hand)

        # Test royal straight non-flush
        a = HandTestUtils.build_shorthand('ac', 'kd', 'qc', 'jc', '10c')
        self.assertFalse(BaseHand(a).as_hand(RoyalFlush).is_hand)

        # Test with multiple straight cards
        a = HandTestUtils.build_shorthand('ac', 'kc', 'qc', 'jc', '10c', '9c', '8c')
        self.assertTrue(BaseHand(a).as_hand(RoyalFlush).is_hand)
        self.assertEqual(BaseHand(a).as_hand(RoyalFlush).cards_in_hand, HandTestUtils.build_shorthand('ac', 'kc', 'qc', 'jc', '10c'))

        # Test with multiple flush non-straight cards
        a = HandTestUtils.build_shorthand('ac', 'kc', 'qc', 'jc', '10c', '5c', '8c')
        self.assertTrue(BaseHand(a).as_hand(RoyalFlush).is_hand)
        self.assertEqual(BaseHand(a).as_hand(RoyalFlush).cards_in_hand, HandTestUtils.build_shorthand('ac', 'kc', 'qc', 'jc', '10c'))

    def test_not_implemented(self):
        HandTestUtils.test_not_implemented(self, RoyalFlush)
