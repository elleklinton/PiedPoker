from unittest import TestCase

from pied_poker.hand import BaseHand
from pied_poker.hand import Straight
from pied_poker.test.unit.hands.hand_test_utils import HandTestUtils


class TestStraight(TestCase):
    def test_comparison(self):
        # Test same straights 5 card_internals hand
        a = HandTestUtils.build_shorthand('2d', '3c', '4h', '5s', '6d')
        b = HandTestUtils.build_shorthand('2d', '3c', '4h', '5s', '6d')
        HandTestUtils.assertEquals(self, Straight, a, b)

        # Test same straights 7 card_internals hand, same other 2
        a = HandTestUtils.build_shorthand('2d', '3c', '4h', '5s', '6d', '10d', 'ks')
        b = HandTestUtils.build_shorthand('2d', '3c', '4h', '5s', '6d', '10d', 'ks')
        HandTestUtils.assertEquals(self, Straight, a, b)

        # Test same straights 7 card_internals hand, different other 2
        a = HandTestUtils.build_shorthand('2d', '3c', '4h', '5s', '6d', 'qd', 'as')
        b = HandTestUtils.build_shorthand('2d', '3c', '4h', '5s', '6d', '10d', 'ks')
        HandTestUtils.assertEquals(self, Straight, a, b)

        # Test same straight different suit top card_internals
        a = HandTestUtils.build_shorthand('2c', '3c', '4c', '5c', '6c', '6s')
        a = HandTestUtils.build_shorthand('2c', '3c', '4c', '5c', '6d', '6h')
        HandTestUtils.assertEquals(self, Straight, a, b)

        # Test mostly same straight with different rank top card_internals
        a = HandTestUtils.build_shorthand('2c', '3c', '4c', '5c', '6c', '7s')
        b = HandTestUtils.build_shorthand('2c', '3c', '4c', '5c', '6d', '6h')
        HandTestUtils.assertGreaterThan(self, Straight, a, b)

        # Test mostly same straight with different rank top card_internals
        a = HandTestUtils.build_shorthand('2c', '3c', '4c', '5c', '6c', '7s')
        b = HandTestUtils.build_shorthand('2c', '3c', '4c', '5c', '6d', '6h')
        HandTestUtils.assertGreaterThan(self, Straight, a, b)

    def test_cards_in_hand(self):
        # Finds correct straight with same top 2
        a = HandTestUtils.build_shorthand('6s', '6c', '5c', '4c', '3c', '2c')
        self.assertEqual(BaseHand(a).as_hand(Straight).cards_in_hand, HandTestUtils.build_shorthand('6s', '5c', '4c', '3c', '2c'))
        self.assertEqual(BaseHand(a).as_hand(Straight).cards_not_in_hand, HandTestUtils.build_shorthand())

        # Finds correct straight with same bottom 2
        a = HandTestUtils.build_shorthand('6s', '5c', '4c', '3c', '2c', '2s')
        self.assertEqual(BaseHand(a).as_hand(Straight).cards_in_hand, HandTestUtils.build_shorthand('6s', '5c', '4c', '3c', '2c'))
        self.assertEqual(BaseHand(a).as_hand(Straight).cards_not_in_hand, HandTestUtils.build_shorthand())

        # Finds correct straight with multiple possible straights
        a = HandTestUtils.build_shorthand('7s', '6c', '6s', '5c', '4c', '3c', '2c')
        self.assertEqual(BaseHand(a).as_hand(Straight).cards_in_hand, HandTestUtils.build_shorthand('7s', '6c', '5c', '4c', '3c'))
        self.assertEqual(BaseHand(a).as_hand(Straight).cards_not_in_hand, HandTestUtils.build_shorthand())

        # Finds correct straight with multiple possible straights
        a = HandTestUtils.build_shorthand('7s', '6c', '6s', '5c', '4c', '3c', '2c')
        self.assertEqual(BaseHand(a).as_hand(Straight).cards_in_hand, HandTestUtils.build_shorthand('7s', '6c', '5c', '4c', '3c'))
        self.assertEqual(BaseHand(a).as_hand(Straight).cards_not_in_hand, HandTestUtils.build_shorthand())

        # Finds correct straight with multiple shared middle cards
        a = HandTestUtils.build_shorthand('7s', '6c', '5s', '5c', '4c', '3c', '3d')
        self.assertEqual(BaseHand(a).as_hand(Straight).cards_in_hand, HandTestUtils.build_shorthand('7s', '6c', '5c', '4c', '3c'))
        self.assertEqual(BaseHand(a).as_hand(Straight).cards_not_in_hand, HandTestUtils.build_shorthand())

        # Finds correct straight with multiple shared middle cards and multiple possible straights
        a = HandTestUtils.build_shorthand('7s', '6c', '5s', '5c', '4c', '3d', '2c')
        self.assertEqual(BaseHand(a).as_hand(Straight).cards_in_hand, HandTestUtils.build_shorthand('7s', '6c', '5c', '4c', '3c'))
        self.assertEqual(BaseHand(a).as_hand(Straight).cards_not_in_hand, HandTestUtils.build_shorthand())

    def test_ace_low_straight(self):
        # Ace straight is found
        a = HandTestUtils.build_shorthand('5s', '4c', '3s', '2d', 'ah')
        self.assertEqual(BaseHand(a).as_hand(Straight).cards_in_hand, HandTestUtils.build_shorthand('5s', '4c', '3s', '2d', 'ah'))
        self.assertEqual(BaseHand(a).as_hand(Straight).cards_not_in_hand, HandTestUtils.build_shorthand())

        # Ace straight is not highest straight
        a = HandTestUtils.build_shorthand('6h', '5s', '4c', '3s', '2d', 'ah')
        self.assertEqual(BaseHand(a).as_hand(Straight).cards_in_hand, HandTestUtils.build_shorthand('6h', '5s', '4c', '3s', '2d'))
        self.assertEqual(BaseHand(a).as_hand(Straight).cards_not_in_hand, HandTestUtils.build_shorthand())

    def test_all_possible_straights(self):
        a = HandTestUtils.build_shorthand('5s', '4c', '3s', '2d', 'ah')
        self.assertEqual(BaseHand(a).as_hand(Straight).cards_in_hand, HandTestUtils.build_shorthand('5s', '4c', '3s', '2d', 'ah'))
        last = a

        a = HandTestUtils.build_shorthand('6s', '5s', '4c', '3s', '2d', 'ah')
        self.assertEqual(BaseHand(a).as_hand(Straight).cards_in_hand, HandTestUtils.build_shorthand('6s', '5s', '4c', '3s', '2d'))
        HandTestUtils.assertGreaterThan(self, Straight, a, last)
        last = a

        a = HandTestUtils.build_shorthand('7c', '6s', '5s', '4c', '3s', '2d', 'ah')
        self.assertEqual(BaseHand(a).as_hand(Straight).cards_in_hand, HandTestUtils.build_shorthand('7c', '6s', '5s', '4c', '3s'))
        HandTestUtils.assertGreaterThan(self, Straight, a, last)
        last = a

        a = HandTestUtils.build_shorthand('8s', '7c', '6s', '5s', '4c', '3s', '2d', 'ah')
        self.assertEqual(BaseHand(a).as_hand(Straight).cards_in_hand, HandTestUtils.build_shorthand('8s', '7c', '6s', '5s', '4c'))
        HandTestUtils.assertGreaterThan(self, Straight, a, last)
        last = a

        a = HandTestUtils.build_shorthand('9c', '8s', '7c', '6s', '5s', '4c', '3s', '2d', 'ah')
        self.assertEqual(BaseHand(a).as_hand(Straight).cards_in_hand, HandTestUtils.build_shorthand('9c', '8s', '7c', '6s', '5s'))
        HandTestUtils.assertGreaterThan(self, Straight, a, last)
        last = a

        a = HandTestUtils.build_shorthand('10s', '9c', '8s', '7c', '6s', '5s', '4c', '3s', '2d', 'ah')
        self.assertEqual(BaseHand(a).as_hand(Straight).cards_in_hand, HandTestUtils.build_shorthand('10s', '9c', '8s', '7c', '6s'))
        HandTestUtils.assertGreaterThan(self, Straight, a, last)
        last = a

        a = HandTestUtils.build_shorthand('jc', '10s', '9c', '8s', '7c', '6s', '5s', '4c', '3s', '2d', 'ah')
        self.assertEqual(BaseHand(a).as_hand(Straight).cards_in_hand, HandTestUtils.build_shorthand('jc', '10s', '9c', '8s', '7c'))
        HandTestUtils.assertGreaterThan(self, Straight, a, last)
        last = a

        a = HandTestUtils.build_shorthand('qc', 'jc', '10s', '9c', '8s', '7c', '6s', '5s', '4c', '3s', '2d', 'ah')
        self.assertEqual(BaseHand(a).as_hand(Straight).cards_in_hand, HandTestUtils.build_shorthand('qc', 'jc', '10s', '9c', '8s'))
        HandTestUtils.assertGreaterThan(self, Straight, a, last)
        last = a

        a = HandTestUtils.build_shorthand('ks', 'qc', 'jc', '10s', '9c', '8s', '7c', '6s', '5s', '4c', '3s', '2d')
        self.assertEqual(BaseHand(a).as_hand(Straight).cards_in_hand, HandTestUtils.build_shorthand('ks', 'qc', 'jc', '10s', '9c'))
        HandTestUtils.assertGreaterThan(self, Straight, a, last)
        last = a

        a = HandTestUtils.build_shorthand('ac', 'ks', 'qc', 'jc', '10s', '9c', '8s', '7c', '6s', '5s', '4c', '3s', '2d')
        self.assertEqual(BaseHand(a).as_hand(Straight).cards_in_hand, HandTestUtils.build_shorthand('ac', 'ks', 'qc', 'jc', '10s'))
        HandTestUtils.assertGreaterThan(self, Straight, a, last)

    def test_non_straight(self):
        a = HandTestUtils.build_shorthand('qc', 'kc', 'ac', '2c', '3c')
        self.assertFalse(BaseHand(a).as_hand(Straight).is_hand)

    def test_not_implemented(self):
        HandTestUtils.test_not_implemented(self, Straight)

    def test_outs(self):
        a = HandTestUtils.build_shorthand('as', 'qd', 'jh', '10c')
        self.assertEqual(BaseHand(a).as_hand(Straight).__hand_outs__(set()), HandTestUtils.build_shorthand(
            'kc', 'kd', 'kh', 'ks'
        ))

        a = HandTestUtils.build_shorthand('kd', 'qh', 'jc', '10h')
        self.assertEqual(BaseHand(a).as_hand(Straight).__hand_outs__(set()), HandTestUtils.build_shorthand(
            '9c', '9d', '9h', '9s', 'ac', 'ad', 'ah', 'as'
        ))

