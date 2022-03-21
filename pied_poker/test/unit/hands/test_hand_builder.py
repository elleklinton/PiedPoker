from unittest import TestCase

from pied_poker.card.card import Card
from pied_poker.test.unit.hands.hand_test_utils import HandTestUtils


class TestHandBuilder(TestCase):
    def test_happy(self):
        hand = HandTestUtils.build_shorthand('2s', '9d', '10h', 'jc', 'ah')
        self.assertEqual(hand[0], Card('2s'))
        self.assertEqual(hand[1], Card('9d'))
        self.assertEqual(hand[2], Card('10h'))
        self.assertEqual(hand[3], Card('jc'))
        self.assertEqual(hand[4], Card('ah'))
