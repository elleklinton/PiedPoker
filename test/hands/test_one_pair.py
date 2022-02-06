from unittest import TestCase

from test.hands.base_hand import BaseHand
from hands.one_pair import OnePair
from test.hands.hand_test_utils import HandTestUtils


class TestOnePair(TestCase):
    def test_comparison(self):
        # Test simple pair with same other cards
        a = HandTestUtils.build_shorthand('2d', '2c', '3h', 'qs', 'kd')
        b = HandTestUtils.build_shorthand('2d', '2c', '3h', 'qs', 'kd')
        HandTestUtils.assertEquals(self, OnePair, a, b)

        # Test simple pair with same top 3 other cards, different final 2
        a = HandTestUtils.build_shorthand('2d', '2c', '10h', 'qs', 'ad',
                                          '7s', '3d')
        b = HandTestUtils.build_shorthand('2d', '2c', '10h', 'qs', 'kd',
                                          '6c', '8c')
        HandTestUtils.assertGreaterThan(self, OnePair, a, b)
        HandTestUtils.assertLessThan(self, OnePair, b, a)

        # Test same pair with different high card_internals
        a = HandTestUtils.build_shorthand('2d', '2c', '3h', 'qs', 'ad')
        b = HandTestUtils.build_shorthand('2d', '2c', '3h', 'qs', 'kd')
        HandTestUtils.assertGreaterThan(self, OnePair, a, b)
        HandTestUtils.assertLessThan(self, OnePair, b, a)

        # Test different pair with same high cards
        a = HandTestUtils.build_shorthand('3d', '3c', '4h', 'qs', 'kd')
        b = HandTestUtils.build_shorthand('2d', '2c', '4h', 'qs', 'kd')
        HandTestUtils.assertGreaterThan(self, OnePair, a, b)
        HandTestUtils.assertLessThan(self, OnePair, b, a)

        # Test different pair with different high cards
        a = HandTestUtils.build_shorthand('3d', '3c', '4h', 'qs', 'kd')
        b = HandTestUtils.build_shorthand('2d', '2c', '4h', 'qs', 'ad')
        HandTestUtils.assertGreaterThan(self, OnePair, a, b)
        HandTestUtils.assertLessThan(self, OnePair, b, a)

    def test_tiebreakers(self):
        # From https://automaticpoker.com/poker-basics/what-happens-if-you-have-the-same-hand-in-poker/
        a = HandTestUtils.build_shorthand('kd', 'kc', '10h', '7s', '5d')
        b = HandTestUtils.build_shorthand('kd', 'kc', '9h', '4s', '2d')
        HandTestUtils.assertGreaterThan(self, OnePair, a, b)
        HandTestUtils.assertLessThan(self, OnePair, b, a)

        a = HandTestUtils.build_shorthand('8d', '8c', '6h', '5s', '2d')
        b = HandTestUtils.build_shorthand('8d', '8c', '6h', '4s', '2d')
        HandTestUtils.assertGreaterThan(self, OnePair, a, b)
        HandTestUtils.assertLessThan(self, OnePair, b, a)

        a = HandTestUtils.build_shorthand('ad', 'ac', 'kh', '8s', '3d')
        b = HandTestUtils.build_shorthand('ad', 'ac', 'kh', '8s', '2d')
        HandTestUtils.assertGreaterThan(self, OnePair, a, b)
        HandTestUtils.assertLessThan(self, OnePair, b, a)

    def test_cards_in_hand(self):
        a = HandTestUtils.build_shorthand('3d', '3c', '6h', 'qs', 'kd',
                                          '4s', '5d')
        # Should pick 2 cards that are a pair
        self.assertEqual(BaseHand(a).as_hand(OnePair).cards_in_hand, HandTestUtils.build_shorthand('3d', '3c'))
        # Should pick next top 3 cards after the pair
        self.assertEqual(BaseHand(a).as_hand(OnePair).cards_not_in_hand, HandTestUtils.build_shorthand('kd', 'qs', '6h'))

    def test_not_implemented(self):
        HandTestUtils.test_not_implemented(self, OnePair)
