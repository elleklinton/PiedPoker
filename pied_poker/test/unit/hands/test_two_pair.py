from unittest import TestCase

from pied_poker.hand import BaseHand
from pied_poker.hand import TwoPair
from pied_poker.test.unit.hands.hand_test_utils import HandTestUtils


class TestTwoPair(TestCase):
    def test_comparison(self):
        # Same exact hand
        a = HandTestUtils.build_shorthand('2d', '2c', '3d', '3c', 'kd', '6c', '5c')
        b = HandTestUtils.build_shorthand('2d', '2c', '3d', '3c', 'kd', '6c', '4c')
        HandTestUtils.assertEquals(self, TwoPair, a, b)

        # Same 2 pairs, different kicker
        a = HandTestUtils.build_shorthand('2d', '2c', '3d', '3c', 'ad')
        b = HandTestUtils.build_shorthand('2d', '2c', '3d', '3c', 'kd')
        HandTestUtils.assertGreaterThan(self, TwoPair, a, b)
        HandTestUtils.assertLessThan(self, TwoPair, b, a)

        # Same top pair, different bottom pair, same kicker
        a = HandTestUtils.build_shorthand('4d', '4c', '3d', '3c', 'kd')
        b = HandTestUtils.build_shorthand('4d', '4c', '2d', '2c', 'kd')
        HandTestUtils.assertGreaterThan(self, TwoPair, a, b)
        HandTestUtils.assertLessThan(self, TwoPair, b, a)

        # Same top pair, different bottom pair, different kicker
        a = HandTestUtils.build_shorthand('4d', '4c', '3d', '3c', 'kd')
        b = HandTestUtils.build_shorthand('4d', '4c', '2d', '2c', 'ad')
        HandTestUtils.assertGreaterThan(self, TwoPair, a, b)
        HandTestUtils.assertLessThan(self, TwoPair, b, a)

        # Different top pair, same bottom pair, same kicker
        a = HandTestUtils.build_shorthand('4d', '4c', '2d', '2c', 'kd')
        b = HandTestUtils.build_shorthand('3d', '3c', '2d', '2c', 'kd')
        HandTestUtils.assertGreaterThan(self, TwoPair, a, b)
        HandTestUtils.assertLessThan(self, TwoPair, b, a)

        # Different top pair, same bottom pair, different kicker
        a = HandTestUtils.build_shorthand('4d', '4c', '2d', '2c', 'kd')
        b = HandTestUtils.build_shorthand('3d', '3c', '2d', '2c', 'ad')
        HandTestUtils.assertGreaterThan(self, TwoPair, a, b)
        HandTestUtils.assertLessThan(self, TwoPair, b, a)

        # Different top pair, different bottom pair, same kicker
        a = HandTestUtils.build_shorthand('6d', '6c', '3d', '3c', 'kd')
        b = HandTestUtils.build_shorthand('5d', '5c', '4d', '4c', 'kd')
        HandTestUtils.assertGreaterThan(self, TwoPair, a, b)
        HandTestUtils.assertLessThan(self, TwoPair, b, a)

        # Different top pair, different bottom pair, different kicker
        a = HandTestUtils.build_shorthand('6d', '6c', '3d', '3c', 'kd')
        b = HandTestUtils.build_shorthand('5d', '5c', '4d', '4c', 'ad')
        HandTestUtils.assertGreaterThan(self, TwoPair, a, b)
        HandTestUtils.assertLessThan(self, TwoPair, b, a)

    def test_tiebreakers(self):
        a = HandTestUtils.build_shorthand('jd', 'jc', '2d', '2c', 'kd')
        b = HandTestUtils.build_shorthand('10d', '10c', '9d', '9c', 'kd')
        HandTestUtils.assertGreaterThan(self, TwoPair, a, b)
        HandTestUtils.assertLessThan(self, TwoPair, b, a)

        a = HandTestUtils.build_shorthand('7d', '7c', '3d', '3c', 'ad')
        b = HandTestUtils.build_shorthand('5d', '5c', '4d', '4c', '2d')
        HandTestUtils.assertGreaterThan(self, TwoPair, a, b)
        HandTestUtils.assertLessThan(self, TwoPair, b, a)

        a = HandTestUtils.build_shorthand('jd', 'jc', '10d', '10c', '8d')
        b = HandTestUtils.build_shorthand('jd', 'jc', '10d', '10c', '5d')
        HandTestUtils.assertGreaterThan(self, TwoPair, a, b)
        HandTestUtils.assertLessThan(self, TwoPair, b, a)

        a = HandTestUtils.build_shorthand('8d', '8c', '2d', '2c', 'ad')
        b = HandTestUtils.build_shorthand('8d', '8c', '2d', '2c', 'kd')
        HandTestUtils.assertGreaterThan(self, TwoPair, a, b)
        HandTestUtils.assertLessThan(self, TwoPair, b, a)

    def test_cards_in_hand(self):
        a = HandTestUtils.build_shorthand('8d', '8c', '2d', '2c', 'ad')
        self.assertEqual(BaseHand(a).__as_hand__(TwoPair).cards_in_hand, HandTestUtils.build_shorthand('8d', '8c', '2d', '2c'))
        self.assertEqual(BaseHand(a).__as_hand__(TwoPair).cards_not_in_hand, HandTestUtils.build_shorthand('ad'))

    def test_not_implemented(self):
        HandTestUtils.test_not_implemented(self, TwoPair)

    def test_outs(self):
        a = HandTestUtils.build_shorthand('as', '10d', '10c', '5c', '2s')

        outs = BaseHand(a).__as_hand__(TwoPair).__hand_outs__(set())

        self.assertEqual(outs, HandTestUtils.build_shorthand(
            'ac', 'ad', 'ah', '5d', '5h', '5s', '2c', '2d', '2h'
        ))
