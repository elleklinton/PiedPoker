from unittest import TestCase

from pied_poker.hand import BaseHand
from pied_poker.hand.flush import Flush
from pied_poker.test.unit.hands.hand_test_utils import HandTestUtils


class TestFlush(TestCase):
    def test_comparisons(self):
        # Test same flush 5 card_internals hand
        a = HandTestUtils.build_shorthand('2d', '4d', '6d', '9d', 'kd')
        b = HandTestUtils.build_shorthand('2d', '4d', '6d', '9d', 'kd')
        HandTestUtils.assertEquals(self, Flush, a, b)

        # Test different flush 5 card_internals hand with same top card
        a = HandTestUtils.build_shorthand('5d', '6d', '7d', '10d', 'kd')
        b = HandTestUtils.build_shorthand('2d', '4d', '6d', '9d', 'kd')
        HandTestUtils.assertGreaterThan(self, Flush, a, b)

        # Test different flush 5 card_internals hand with different top card
        a = HandTestUtils.build_shorthand('5d', '6d', '7d', '10d', 'ad')
        b = HandTestUtils.build_shorthand('2d', '4d', '6d', '9d', 'kd')
        HandTestUtils.assertGreaterThan(self, Flush, a, b)

        # Test same flush 5 card_internals hand diff suits
        a = HandTestUtils.build_shorthand('2d', '4d', '6d', '9d', 'kd')
        b = HandTestUtils.build_shorthand('2s', '4s', '6s', '9s', 'ks')
        HandTestUtils.assertEquals(self, Flush, a, b)

        # Test diff flush 5 card_internals hand diff suits same top card
        a = HandTestUtils.build_shorthand('5d', '6d', '7d', '10d', 'kd')
        b = HandTestUtils.build_shorthand('2s', '4s', '6s', '9s', 'ks')
        HandTestUtils.assertGreaterThan(self, Flush, a, b)

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

    def test_same_high_card_are_not_equal(self):
        c1 = HandTestUtils.build_shorthand('ks', 'qs', '9s', '8s', '7s')
        c2 = HandTestUtils.build_shorthand('ks', 'qs', '8s', '7s', '4s')

        h1 = BaseHand(c1).as_hand(Flush)
        h2 = BaseHand(c2).as_hand(Flush)

        self.assertTrue(h1 != h2)
        self.assertFalse(h1 == h2)
        self.assertTrue(h1 > h2)
        self.assertFalse(h1 < h2)
        self.assertTrue(h2 < h1)
        self.assertFalse(h2 > h1)

    def test_not_implemented(self):
        HandTestUtils.test_not_implemented(self, Flush)

    def test_outs(self):
        a = HandTestUtils.build_shorthand('as', '9s', '7s', '5s', '10d')

        self.assertEqual(BaseHand(a).as_hand(Flush).__hand_outs__(set()), HandTestUtils.build_shorthand(
            '2s', '3s', '4s', '6s', '8s', '10s', 'js', 'qs', 'ks'
        ))

    def test_diff_number_flush_cards(self):
        tableCards = HandTestUtils.build_shorthand('6d', 'qd', 'ad', '4d', '10s')
        c1 = HandTestUtils.build_shorthand('kd', '3h')
        c2 = HandTestUtils.build_shorthand('7d', '9d')

        h1 = BaseHand(tableCards + c1).as_hand(Flush)
        h2 = BaseHand(tableCards + c2).as_hand(Flush)

        self.assertTrue(h1 != h2)
        self.assertFalse(h1 == h2)
        self.assertTrue(h1 > h2)
        self.assertFalse(h1 < h2)
        self.assertTrue(h2 < h1)
        self.assertFalse(h2 > h1)
