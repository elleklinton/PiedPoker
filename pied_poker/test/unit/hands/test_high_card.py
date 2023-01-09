from unittest import TestCase

from pied_poker.hand import BaseHand
from pied_poker.hand import HighCard
from pied_poker.test.unit.hands.hand_test_utils import HandTestUtils


class TestHighCard(TestCase):
    def test_comparisons(self):
        # Same exact 5 card_internals hand
        a = HandTestUtils.build_shorthand('2d', '10c', '3h', 'qs', 'kd')
        b = HandTestUtils.build_shorthand('2d', '10c', '3h', 'qs', 'kd')
        HandTestUtils.assertEquals(self, HighCard, a, b)

        # Same top 5 cards same bottom 2 cards: should be equal ranked hands
        a = HandTestUtils.build_shorthand('7d', '8d', '10d', 'qd', 'kd',
                                          '6d', '5d')
        b = HandTestUtils.build_shorthand('7c', '8c', '10c', 'qc', 'kc',
                                          '6c', '5c')
        HandTestUtils.assertEquals(self, HighCard, a, b)

        # Same top 5 cards different bottom 2 cards: should be equal ranked hands
        a = HandTestUtils.build_shorthand('7d', '8d', '10d', 'qd', 'kd',
                                          '6d', '5d')
        b = HandTestUtils.build_shorthand('7c', '8c', '10c', 'qc', 'kc',
                                          '3c', '4c')
        HandTestUtils.assertEquals(self, HighCard, a, b)

        # Same hand, except top card_internals is different
        a = HandTestUtils.build_shorthand('7d', '8d', '10d', 'qd', 'ad',
                                          '6d', '5d')
        b = HandTestUtils.build_shorthand('7c', '8c', '10c', 'qc', 'kc',
                                          '6c', '5c')
        HandTestUtils.assertGreaterThan(self, HighCard, a, b)
        HandTestUtils.assertLessThan(self, HighCard, b, a)

        # Same top 4 ranks, 5th rank is different
        a = HandTestUtils.build_shorthand('7d', '8d', '10d', 'qd', 'kd',
                                          '3d', '4d')
        b = HandTestUtils.build_shorthand('6c', '8c', '10c', 'qc', 'kc',
                                          '3c', '4c')
        HandTestUtils.assertGreaterThan(self, HighCard, a, b)
        HandTestUtils.assertLessThan(self, HighCard, b, a)

        # Test high card > Base hand not initialized with anything
        a = HandTestUtils.build_shorthand('7d', '8d', '10d', 'qd', 'kd',
                                          '3d', '4d')
        self.assertGreater(BaseHand(a).as_hand(HighCard), BaseHand(a))
        self.assertFalse(BaseHand(a).as_hand(HighCard) < BaseHand(a))
        self.assertLess(BaseHand(a), BaseHand(a).as_hand(HighCard))
        self.assertFalse(BaseHand(a) > BaseHand(a).as_hand(HighCard))

    def test_tiebreakers(self):
        # From https://automaticpoker.com/poker-basics/what-happens-if-you-have-the-same-hand-in-poker/
        a = HandTestUtils.build_shorthand('ad', 'jd', '10d', '8d', '5d')
        b = HandTestUtils.build_shorthand('ad', 'jd', '10d', '8d', '2d')
        HandTestUtils.assertGreaterThan(self, HighCard, a, b)
        HandTestUtils.assertLessThan(self, HighCard, b, a)

        a = HandTestUtils.build_shorthand('10d', '8d', '5d', '4d', '2d')
        b = HandTestUtils.build_shorthand('10d', '7d', '6d', '5d', '3d')
        HandTestUtils.assertGreaterThan(self, HighCard, a, b)
        HandTestUtils.assertLessThan(self, HighCard, b, a)

        a = HandTestUtils.build_shorthand('8d', '5d', '4d', '3d', '2d')
        b = HandTestUtils.build_shorthand('7d', '6d', '5d', '4d', '2d')
        HandTestUtils.assertGreaterThan(self, HighCard, a, b)
        HandTestUtils.assertLessThan(self, HighCard, b, a)

        a = HandTestUtils.build_shorthand('kd', '6d', '5d', '4d', '2d')
        b = HandTestUtils.build_shorthand('kd', '6d', '5d', '3d', '2d')
        HandTestUtils.assertGreaterThan(self, HighCard, a, b)
        HandTestUtils.assertLessThan(self, HighCard, b, a)

    def test_cards_in_hand(self):
        a = HandTestUtils.build_shorthand('7d', '8d', '10d', 'qd', 'kd',
                                          '3d', '4d')
        # Should pick top 5 cards in descending order
        self.assertEqual(BaseHand(a).as_hand(HighCard).cards_in_hand, HandTestUtils.build_shorthand('kd', 'qd', '10d', '8d', '7d'))
        # Should exclude last 2 cards
        self.assertEqual(BaseHand(a).as_hand(HighCard).cards_not_in_hand, HandTestUtils.build_shorthand('4d', '3d'))

    def test_not_implemented(self):
        HandTestUtils.test_not_implemented(self, HighCard)

    def test_outs(self):
        a = HandTestUtils.build_shorthand('10s')

        outs = BaseHand(a).as_hand(HighCard).__hand_outs__()
        self.assertEqual(outs, HandTestUtils.build_shorthand(
            'jc', 'jd', 'jh', 'js', 'qc', 'qd', 'qh', 'qs', 'kc', 'kd', 'kh', 'ks', 'ac', 'ad', 'ah', 'as'
        ))

