from unittest import TestCase

from hands.base_hand import BaseHand
from hands.flush import Flush
from test.hands.hand_test_utils import HandTestUtils


class TestFlush(TestCase):
    def test_comparisons(self):
        # Test same flush 5 card_internals hand
        a = HandTestUtils.build_shorthand('2d', '4d', '6d', '9d', 'kd')
        b = HandTestUtils.build_shorthand('2d', '4d', '6d', '9d', 'kd')
        HandTestUtils.assertEquals(self, Flush, a, b)

        # Test different flush 5 card_internals hand with same top card_internals
        a = HandTestUtils.build_shorthand('5d', '6d', '7d', '10d', 'kd')
        b = HandTestUtils.build_shorthand('2d', '4d', '6d', '9d', 'kd')
        HandTestUtils.assertEquals(self, Flush, a, b)

        # Test different flush 5 card_internals hand with different top card_internals
        a = HandTestUtils.build_shorthand('5d', '6d', '7d', '10d', 'ad')
        b = HandTestUtils.build_shorthand('2d', '4d', '6d', '9d', 'kd')
        HandTestUtils.assertGreaterThan(self, Flush, a, b)

        # Test same flush 5 card_internals hand diff suits
        a = HandTestUtils.build_shorthand('2d', '4d', '6d', '9d', 'kd')
        b = HandTestUtils.build_shorthand('2s', '4s', '6s', '9s', 'ks')
        HandTestUtils.assertEquals(self, Flush, a, b)

        # Test diff flush 5 card_internals hand diff suits same top card_internals
        a = HandTestUtils.build_shorthand('5d', '6d', '7d', '10d', 'kd')
        b = HandTestUtils.build_shorthand('2s', '4s', '6s', '9s', 'ks')
        HandTestUtils.assertEquals(self, Flush, a, b)

        # Test diff suits diff high card_internals
        a = HandTestUtils.build_shorthand('5d', '6d', '7d', '10d', 'ad')
        b = HandTestUtils.build_shorthand('2s', '4s', '6s', '9s', 'ks')
        HandTestUtils.assertGreaterThan(self, Flush, a, b)

        # Test diff suits diff high card_internals with extra non-suited cards
        a = HandTestUtils.build_shorthand('5d', '6d', '7d', '10d', 'ad', 'js', 'ks')
        b = HandTestUtils.build_shorthand('2s', '4s', '6s', '9s', 'ks', '10d', 'ad')
        HandTestUtils.assertGreaterThan(self, Flush, a, b)

    def test_cards_in_hand(self):
        # Finds all diamonds
        a = HandTestUtils.build_shorthand('5d', '6d', '7d', '10d', 'ad', 'js', 'ks')
        self.assertEqual(BaseHand(a).as_hand(Flush).cards_in_hand, HandTestUtils.build_shorthand('ad', '10d', '7d', '6d', '5d'))
        self.assertEqual(BaseHand(a).as_hand(Flush).cards_not_in_hand, HandTestUtils.build_shorthand())

        # Finds highest diamonds
        a = HandTestUtils.build_shorthand('2d', '5d', '6d', '7d', '10d', 'ad', 'js', 'ks')
        self.assertEqual(BaseHand(a).as_hand(Flush).cards_in_hand, HandTestUtils.build_shorthand('ad', '10d', '7d', '6d', '5d'))
        self.assertEqual(BaseHand(a).as_hand(Flush).cards_not_in_hand, HandTestUtils.build_shorthand())

    def test_not_implemented(self):
        HandTestUtils.test_not_implemented(self, Flush)
