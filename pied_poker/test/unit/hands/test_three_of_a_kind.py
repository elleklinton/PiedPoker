from unittest import TestCase

from pied_poker.hand import BaseHand
from pied_poker.hand import ThreeOfAKind
from pied_poker.test.unit.hands.hand_test_utils import HandTestUtils


class TestThreeOfAKind(TestCase):
    def test_comparison(self):
        # Same exact hand
        a = HandTestUtils.build_shorthand('2d', '2c', '2h', '3c', 'kd')
        b = HandTestUtils.build_shorthand('2d', '2c', '2h', '3c', 'kd')
        HandTestUtils.assertEquals(self, ThreeOfAKind, a, b)

        # Same trips different high card_internals kicker
        a = HandTestUtils.build_shorthand('2d', '2c', '2h', '3c', 'ad')
        b = HandTestUtils.build_shorthand('2d', '2c', '2h', '3c', 'kd')
        HandTestUtils.assertGreaterThan(self, ThreeOfAKind, a, b)
        HandTestUtils.assertLessThan(self, ThreeOfAKind, b, a)

        # Same trips different low card_internals kicker
        a = HandTestUtils.build_shorthand('2d', '2c', '2h', '4c', 'kd')
        b = HandTestUtils.build_shorthand('2d', '2c', '2h', '3c', 'kd')
        HandTestUtils.assertGreaterThan(self, ThreeOfAKind, a, b)
        HandTestUtils.assertLessThan(self, ThreeOfAKind, b, a)

        # Different trips, same other cards
        a = HandTestUtils.build_shorthand('6d', '6c', '6h', '3c', 'kd')
        b = HandTestUtils.build_shorthand('2d', '2c', '2h', '3c', 'kd')
        HandTestUtils.assertGreaterThan(self, ThreeOfAKind, a, b)
        HandTestUtils.assertLessThan(self, ThreeOfAKind, b, a)

        # Different trips, different other cards
        a = HandTestUtils.build_shorthand('6d', '6c', '6h', '3c', 'kd')
        b = HandTestUtils.build_shorthand('2d', '2c', '2h', '3c', 'ad')
        HandTestUtils.assertGreaterThan(self, ThreeOfAKind, a, b)
        HandTestUtils.assertLessThan(self, ThreeOfAKind, b, a)

    def test_tiebreakers(self):
        a = HandTestUtils.build_shorthand('10d', '10c', '10h', '9c', '2d')
        b = HandTestUtils.build_shorthand('7d', '7c', '7h', '4c', '3d')
        HandTestUtils.assertGreaterThan(self, ThreeOfAKind, a, b)
        HandTestUtils.assertLessThan(self, ThreeOfAKind, b, a)

        a = HandTestUtils.build_shorthand('qd', 'qc', 'qh', '10c', '2d')
        b = HandTestUtils.build_shorthand('qd', 'qc', 'qh', '7c', '6d')
        HandTestUtils.assertGreaterThan(self, ThreeOfAKind, a, b)
        HandTestUtils.assertLessThan(self, ThreeOfAKind, b, a)

    def test_cards_in_hand(self):
        a = HandTestUtils.build_shorthand('8d', '8c', '8h', '2c', 'ad', 'kh', 'js')
        self.assertEqual(BaseHand(a).as_hand(ThreeOfAKind).cards_in_hand, HandTestUtils.build_shorthand('8d', '8c', '8h'))
        self.assertEqual(BaseHand(a).as_hand(ThreeOfAKind).cards_not_in_hand, HandTestUtils.build_shorthand('ad', 'kh'))

    def test_not_implemented(self):
        HandTestUtils.test_not_implemented(self, ThreeOfAKind)
