from unittest import TestCase

from pied_poker.hand import BaseHand
from pied_poker.hand import FourOfAKind
from pied_poker.test.unit.hands.hand_test_utils import HandTestUtils


class TestFourOfAKind(TestCase):
    def test_comparison(self):
        # Test same 4 of a kind
        a = HandTestUtils.build_shorthand('3h', '3d', '3c', '3s', 'ad', 'kd', '10d')
        b = HandTestUtils.build_shorthand('3h', '3d', '3c', '3s', 'ad', 'kd', '10d')
        HandTestUtils.assertEquals(self, FourOfAKind, a, b)

        # Test same 4 of a kind different kickers
        a = HandTestUtils.build_shorthand('3h', '3d', '3c', '3s', 'ad', 'kd', '10d')
        b = HandTestUtils.build_shorthand('3h', '3d', '3c', '3s', '10d', 'kd', '10d')
        HandTestUtils.assertGreaterThan(self, FourOfAKind, a, b)

        # Test different 4 of a kind
        a = HandTestUtils.build_shorthand('ah', 'ad', 'ac', 'as', '10d', 'kd', '10d')
        b = HandTestUtils.build_shorthand('3h', '3d', '3c', '3s', '10d', 'kd', '10d')
        HandTestUtils.assertGreaterThan(self, FourOfAKind, a, b)

        # Test different 4 of a kind different kickers
        a = HandTestUtils.build_shorthand('ah', 'ad', 'ac', 'as', '3d', '4d', '5d')
        b = HandTestUtils.build_shorthand('3h', '3d', '3c', '3s', 'ad', '5d', '4d')
        HandTestUtils.assertGreaterThan(self, FourOfAKind, a, b)

    def test_cards_in_hand(self):
        a = HandTestUtils.build_shorthand('ah', 'ad', 'ac', 'as', '3d', '4d', '5d')
        self.assertEqual(BaseHand(a).as_hand(FourOfAKind).cards_in_hand, HandTestUtils.build_shorthand('ah', 'ad', 'ac', 'as'))
        self.assertEqual(BaseHand(a).as_hand(FourOfAKind).cards_not_in_hand, HandTestUtils.build_shorthand('5d'))

        a = HandTestUtils.build_shorthand('3h', '3d', '3c', '3s', '10d', 'ad', '10d')
        self.assertEqual(BaseHand(a).as_hand(FourOfAKind).cards_in_hand, HandTestUtils.build_shorthand('3h', '3d', '3c', '3s'))
        self.assertEqual(BaseHand(a).as_hand(FourOfAKind).cards_not_in_hand, HandTestUtils.build_shorthand('ad'))

    def test_not_implemented(self):
        HandTestUtils.test_not_implemented(self, FourOfAKind)

    def test_outs(self):
        a = HandTestUtils.build_shorthand('as', 'ac', 'ad', '2s', '2h', '2d', '5c', '8c')

        self.assertEqual(BaseHand(a).as_hand(FourOfAKind).__hand_outs__(set()), HandTestUtils.build_shorthand(
            'ah', '2c'
        ))
