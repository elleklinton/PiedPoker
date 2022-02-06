from unittest import TestCase

from test.hands.base_hand import BaseHand
from hands.full_house import FullHouse
from test.hands.hand_test_utils import HandTestUtils


class TestFullHouse(TestCase):
    def test_comparisons(self):
        # Test same full house
        a = HandTestUtils.build_shorthand('2d', '2c', '3d', '3c', '3s', 'ad', 'kd')
        b = HandTestUtils.build_shorthand('2d', '2c', '3d', '3c', '3s', 'ad', 'kd')
        HandTestUtils.assertEquals(self, FullHouse, a, b)

        # Test same full house different 6/7 cards
        a = HandTestUtils.build_shorthand('2d', '2c', '3d', '3c', '3s', 'ad', 'kd')
        b = HandTestUtils.build_shorthand('2d', '2c', '3d', '3c', '3s', '4d', '5d')
        HandTestUtils.assertEquals(self, FullHouse, a, b)

        # Test same trips, different pair
        a = HandTestUtils.build_shorthand('4d', '4c', '3d', '3c', '3s', 'ad', 'kd')
        b = HandTestUtils.build_shorthand('2d', '2c', '3d', '3c', '3s', 'ad', 'kd')
        HandTestUtils.assertGreaterThan(self, FullHouse, a, b)

        # Test different trips, same pair
        a = HandTestUtils.build_shorthand('2d', '2c', 'kd', 'kc', 'ks', 'ad', '3d')
        b = HandTestUtils.build_shorthand('2d', '2c', '3d', '3c', '3s', 'ad', 'kd')
        HandTestUtils.assertGreaterThan(self, FullHouse, a, b)

        # Test different trips, different pair
        a = HandTestUtils.build_shorthand('2d', '2c', 'kd', 'kc', 'ks', 'ad', '3d')
        b = HandTestUtils.build_shorthand('ad', 'ac', '3d', '3c', '3s', '10d', 'kd')
        HandTestUtils.assertGreaterThan(self, FullHouse, a, b)

    def test_cards_in_hand(self):
        a = HandTestUtils.build_shorthand('2d', '2c', 'kd', 'kc', 'ks', 'ad', '3d')
        self.assertEqual(BaseHand(a).as_hand(FullHouse).cards_in_hand, HandTestUtils.build_shorthand('kd', 'kc', 'ks', '2d', '2c'))
        self.assertEqual(BaseHand(a).as_hand(FullHouse).cards_not_in_hand, HandTestUtils.build_shorthand())

        a = HandTestUtils.build_shorthand('ad', 'ac', '3d', '3c', '3s', '10d', 'kd')
        self.assertEqual(BaseHand(a).as_hand(FullHouse).cards_in_hand, HandTestUtils.build_shorthand('ad', 'ac', '3d', '3c', '3s'))
        self.assertEqual(BaseHand(a).as_hand(FullHouse).cards_not_in_hand, HandTestUtils.build_shorthand())

    def test_tiebreakers(self):
        a = HandTestUtils.build_shorthand('td', 'tc', 'td', '2c', '2s', 'ad', '3d')
        b = HandTestUtils.build_shorthand('7d', '7c', '7d', 'ac', 'as', '10d', 'kd')
        HandTestUtils.assertGreaterThan(self, FullHouse, a, b)

        a = HandTestUtils.build_shorthand('5d', '5c', '5d', 'jc', 'js', 'ad', '3d')
        b = HandTestUtils.build_shorthand('4d', '4c', '4d', 'kc', 'ks', '10d', '3d')
        HandTestUtils.assertGreaterThan(self, FullHouse, a, b)

        a = HandTestUtils.build_shorthand('qd', 'qc', 'qd', '3c', '3s', 'ad', '2d')
        b = HandTestUtils.build_shorthand('qd', 'qc', 'qd', '2c', '2s', '10d', 'kd')
        HandTestUtils.assertGreaterThan(self, FullHouse, a, b)

    def test_not_implemented(self):
        HandTestUtils.test_not_implemented(self, FullHouse)
