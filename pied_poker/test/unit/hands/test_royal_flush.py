from unittest import TestCase

from pied_poker.hand import BaseHand
from pied_poker.hand import RoyalFlush
from pied_poker.test.unit.hands.hand_test_utils import HandTestUtils


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
        self.assertLess(BaseHand(a).__as_hand__(RoyalFlush), BaseHand(a).__as_hand__(FakeHigherHand))
        self.assertFalse(BaseHand(a).__as_hand__(RoyalFlush) > BaseHand(a).__as_hand__(FakeHigherHand))
        self.assertGreater(BaseHand(a).__as_hand__(FakeHigherHand), BaseHand(a).__as_hand__(RoyalFlush))
        self.assertFalse(BaseHand(a).__as_hand__(FakeHigherHand) < BaseHand(a).__as_hand__(RoyalFlush))

    def test_is_hand(self):
        # Test non-royal straight flush
        a = HandTestUtils.build_shorthand('kc', 'qc', 'jc', '10c', '9c')
        self.assertFalse(BaseHand(a).__as_hand__(RoyalFlush).is_hand)

        # Test royal non-straight flush
        a = HandTestUtils.build_shorthand('ac', 'kc', 'jc', '10c', '9c')
        self.assertFalse(BaseHand(a).__as_hand__(RoyalFlush).is_hand)

        # Test royal straight non-flush
        a = HandTestUtils.build_shorthand('ac', 'kd', 'qc', 'jc', '10c')
        self.assertFalse(BaseHand(a).__as_hand__(RoyalFlush).is_hand)

        # Test with multiple straight cards
        a = HandTestUtils.build_shorthand('ac', 'kc', 'qc', 'jc', '10c', '9c', '8c')
        self.assertTrue(BaseHand(a).__as_hand__(RoyalFlush).is_hand)
        self.assertEqual(BaseHand(a).__as_hand__(RoyalFlush).cards_in_hand, HandTestUtils.build_shorthand('ac', 'kc', 'qc', 'jc', '10c'))

        # Test with multiple flush non-straight cards
        a = HandTestUtils.build_shorthand('ac', 'kc', 'qc', 'jc', '10c', '5c', '8c')
        self.assertTrue(BaseHand(a).__as_hand__(RoyalFlush).is_hand)
        self.assertEqual(BaseHand(a).__as_hand__(RoyalFlush).cards_in_hand, HandTestUtils.build_shorthand('ac', 'kc', 'qc', 'jc', '10c'))

    def test_not_implemented(self):
        HandTestUtils.test_not_implemented(self, RoyalFlush)

    def test_outs(self):
        a = HandTestUtils.build_shorthand('as', 'qs', 'js', '10s')
        self.assertEqual(BaseHand(a).__as_hand__(RoyalFlush).__hand_outs__(set()), HandTestUtils.build_shorthand('ks'))

        a = HandTestUtils.build_shorthand('ks', 'qs', 'js', '10s')
        self.assertEqual(BaseHand(a).__as_hand__(RoyalFlush).__hand_outs__(set()), HandTestUtils.build_shorthand('as'))

        a = HandTestUtils.build_shorthand('as', 'ks', 'qs', 'js')
        self.assertEqual(BaseHand(a).__as_hand__(RoyalFlush).__hand_outs__(set()), HandTestUtils.build_shorthand('10s'))
