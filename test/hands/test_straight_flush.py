from unittest import TestCase

from test.hands.base_hand import BaseHand
from hands.straight_flush import StraightFlush
from test.hands.hand_test_utils import HandTestUtils


class TestStraightFlush(TestCase):
    def test_comparisons(self):
        # Test same straights same suit
        a = HandTestUtils.build_shorthand('2d', '3d', '4d', '5d', '6d', '10s', 'ad')
        b = HandTestUtils.build_shorthand('2d', '3d', '4d', '5d', '6d', '10s', 'ad')
        HandTestUtils.assertEquals(self, StraightFlush, a, b)

        # Test same straights different suits
        a = HandTestUtils.build_shorthand('2d', '3d', '4d', '5d', '6d', '10s', 'ad')
        b = HandTestUtils.build_shorthand('2c', '3c', '4c', '5c', '6c', '10s', 'ac')
        HandTestUtils.assertEquals(self, StraightFlush, a, b)

        # Test different high card_internals
        a = HandTestUtils.build_shorthand('3d', '4d', '5d', '6d', '7d', '10s', 'ad')
        b = HandTestUtils.build_shorthand('2c', '3c', '4c', '5c', '6c', '10s', 'ac')
        HandTestUtils.assertGreaterThan(self, StraightFlush, a, b)

        # Test different high card_internals with multiple possible straight flushes
        a = HandTestUtils.build_shorthand('2d', '3d', '4d', '5d', '6d', '7d', '10s', 'ad')
        b = HandTestUtils.build_shorthand('2c', '3c', '4c', '5c', '6c', '10s', 'ac')
        HandTestUtils.assertGreaterThan(self, StraightFlush, a, b)

        # Test higher non-flush straight
        a = HandTestUtils.build_shorthand('2d', '3d', '4d', '5d', '6d', '7s', '10s', 'ad')
        b = HandTestUtils.build_shorthand('2c', '3c', '4c', '5c', '6c', '10s', 'ac')
        HandTestUtils.assertEquals(self, StraightFlush, a, b)

    def test_cards_in_hand(self):
        # Picks correct straight flush
        a = HandTestUtils.build_shorthand('6s', '6c', '5c', '4c', '3c', '2c')
        self.assertEqual(BaseHand(a).as_hand(StraightFlush).cards_in_hand,HandTestUtils.build_shorthand('6c', '5c', '4c', '3c', '2c'))
        self.assertEqual(BaseHand(a).as_hand(StraightFlush).cards_not_in_hand, HandTestUtils.build_shorthand())

        # Test multiple possible, picks highest one
        a = HandTestUtils.build_shorthand('7c', '6c', '5c', '4c', '3c', '2c')
        self.assertEqual(BaseHand(a).as_hand(StraightFlush).cards_in_hand, HandTestUtils.build_shorthand('7c', '6c', '5c', '4c', '3c'))
        self.assertEqual(BaseHand(a).as_hand(StraightFlush).cards_not_in_hand, HandTestUtils.build_shorthand())

    def test_all_possible_straight_flushes(self):
        a = HandTestUtils.build_shorthand('5c', '4c', '3c', '2c', 'ac')
        self.assertEqual(BaseHand(a).as_hand(StraightFlush).cards_in_hand, HandTestUtils.build_shorthand('5c', '4c', '3c', '2c', 'ac'))
        last = a

        a = HandTestUtils.build_shorthand('6c', '5c', '4c', '3c', '2c', 'ac')
        self.assertEqual(BaseHand(a).as_hand(StraightFlush).cards_in_hand, HandTestUtils.build_shorthand('6c', '5c', '4c', '3c', '2c'))
        HandTestUtils.assertGreaterThan(self, StraightFlush, a, last)
        last = a

        a = HandTestUtils.build_shorthand('7c', '6c', '5c', '4c', '3c', '2c', 'ac')
        self.assertEqual(BaseHand(a).as_hand(StraightFlush).cards_in_hand, HandTestUtils.build_shorthand('7c', '6c', '5c', '4c', '3c'))
        HandTestUtils.assertGreaterThan(self, StraightFlush, a, last)
        last = a

        a = HandTestUtils.build_shorthand('8c', '7c', '6c', '5c', '4c', '3c', '2c', 'ac')
        self.assertEqual(BaseHand(a).as_hand(StraightFlush).cards_in_hand, HandTestUtils.build_shorthand('8c', '7c', '6c', '5c', '4c'))
        HandTestUtils.assertGreaterThan(self, StraightFlush, a, last)
        last = a

        a = HandTestUtils.build_shorthand('9c', '8c', '7c', '6c', '5c', '4c', '3c', '2c', 'ac')
        self.assertEqual(BaseHand(a).as_hand(StraightFlush).cards_in_hand, HandTestUtils.build_shorthand('9c', '8c', '7c', '6c', '5c'))
        HandTestUtils.assertGreaterThan(self, StraightFlush, a, last)
        last = a

        a = HandTestUtils.build_shorthand('10c', '9c', '8c', '7c', '6c', '5c', '4c', '3c', '2c', 'ac')
        self.assertEqual(BaseHand(a).as_hand(StraightFlush).cards_in_hand, HandTestUtils.build_shorthand('10c', '9c', '8c', '7c', '6c'))
        HandTestUtils.assertGreaterThan(self, StraightFlush, a, last)
        last = a

        a = HandTestUtils.build_shorthand('jc', '10c', '9c', '8c', '7c', '6c', '5c', '4c', '3c', '2c', 'ac')
        self.assertEqual(BaseHand(a).as_hand(StraightFlush).cards_in_hand, HandTestUtils.build_shorthand('jc', '10c', '9c', '8c', '7c'))
        HandTestUtils.assertGreaterThan(self, StraightFlush, a, last)
        last = a

        a = HandTestUtils.build_shorthand('qc', 'jc', '10c', '9c', '8c', '7c', '6c', '5c', '4c', '3c', '2c', 'ac')
        self.assertEqual(BaseHand(a).as_hand(StraightFlush).cards_in_hand, HandTestUtils.build_shorthand('qc', 'jc', '10c', '9c', '8c'))
        HandTestUtils.assertGreaterThan(self, StraightFlush, a, last)
        last = a

        a = HandTestUtils.build_shorthand('kc', 'qc', 'jc', '10c', '9c', '8c', '7c', '6c', '5c', '4c', '3c', '2c')
        self.assertEqual(BaseHand(a).as_hand(StraightFlush).cards_in_hand, HandTestUtils.build_shorthand('kc', 'qc', 'jc', '10c', '9c'))
        HandTestUtils.assertGreaterThan(self, StraightFlush, a, last)
        last = a

        a = HandTestUtils.build_shorthand('ac', 'kc', 'qc', 'jc', '10c', '9c', '8c', '7c', '6c', '5c', '4c', '3c', '2c')
        self.assertEqual(BaseHand(a).as_hand(StraightFlush).cards_in_hand, HandTestUtils.build_shorthand('ac', 'kc', 'qc', 'jc', '10c'))
        HandTestUtils.assertGreaterThan(self, StraightFlush, a, last)

    def test_non_straight_flush(self):
        # Not a straight
        a = HandTestUtils.build_shorthand('qc', 'kc', 'ac', '2c', '3c')
        self.assertFalse(BaseHand(a).as_hand(StraightFlush).is_hand)

        # Not a flush
        a = HandTestUtils.build_shorthand('10c', 'js', 'qc', 'kc', 'ac')
        self.assertFalse(BaseHand(a).as_hand(StraightFlush).is_hand)

    def test_not_implemented(self):
        HandTestUtils.test_not_implemented(self, StraightFlush)
