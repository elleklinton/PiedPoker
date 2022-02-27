from unittest import TestCase

from card_internals.card import Card
from card_internals.rank import Rank
from card_internals.suit import Suit


class TestCard(TestCase):
    RANK_ALLOWED_VALUES = [v for v in Rank.ALLOWED_VALUES if v != 't']

    def test_init_invalid_rank(self):
        try:
            Card('1', 'c')
        except AssertionError as e:
            e: AssertionError
            self.assertEqual(len(e.args), 1)
            self.assertEqual(e.args[0], 'Invalid Value: 1')

    def test_init_invalid_suit(self):
        try:
            Card('2', 'z')
        except AssertionError as e:
            e: AssertionError
            self.assertEqual(len(e.args), 1)
            self.assertEqual(e.args[0], 'Invalid Value: z')

    def test_init_happy(self):
        for r in Rank.ALLOWED_VALUES:
            for s in Suit.ALLOWED_VALUES:
                Card(r, s)
                Card(r + s)

    def test_str_repr(self):
        self.assertEqual(Card('as').__str__(), 'A♠')
        self.assertEqual(Card('kd').__str__(), 'K♦')
        self.assertEqual(Card('qc').__str__(), 'Q♣')
        self.assertEqual(Card('jh').__str__(), 'J♥')
        self.assertEqual(Card('10h').__str__(), '10♥')
        self.assertEqual(Card('9h').__str__(), '9♥')

        self.assertEqual(Card('as').__repr__(), 'A♠')
        self.assertEqual(Card('kd').__repr__(), 'K♦')
        self.assertEqual(Card('qc').__repr__(), 'Q♣')
        self.assertEqual(Card('jh').__repr__(), 'J♥')
        self.assertEqual(Card('10h').__repr__(), '10♥')
        self.assertEqual(Card('9h').__repr__(), '9♥')

    def test_eq(self):
        for r in Rank.ALLOWED_VALUES:
            for s in Suit.ALLOWED_VALUES:
                a = Card(r, s)
                b = Card(r, s)

                self.assertEqual(a, b)

        for r in Rank.ALLOWED_VALUES:  # Same rank with different suit should be equal
            for i in range(len(Suit.ALLOWED_VALUES) - 1):
                a = Card(r, Suit.ALLOWED_VALUES[i])
                b = Card(r, Suit.ALLOWED_VALUES[i + 1])
                self.assertEqual(a, b)

        for i in range(len(self.RANK_ALLOWED_VALUES) - 1):  # Different rank with same suit should not be equal
            for s in Suit.ALLOWED_VALUES:
                a = Card(self.RANK_ALLOWED_VALUES[i], s)
                b = Card(self.RANK_ALLOWED_VALUES[i + 1], s)
                self.assertNotEqual(a, b)

    def test_gt(self):
        for r in self.RANK_ALLOWED_VALUES:
            for s in Suit.ALLOWED_VALUES:
                a = Card(r, s)
                b = Card(r, s)

                self.assertFalse(a > b)
                self.assertFalse(b > a)

        for r in Rank.ALLOWED_VALUES:  # Same rank with different suit should be equal
            for i in range(len(Suit.ALLOWED_VALUES) - 1):
                a = Card(r, Suit.ALLOWED_VALUES[i])
                b = Card(r, Suit.ALLOWED_VALUES[i + 1])
                self.assertFalse(a > b)
                self.assertFalse(b > a)

        for i in range(len(self.RANK_ALLOWED_VALUES) - 1):  # Different rank with same suit should not be equal
            for s in Suit.ALLOWED_VALUES:
                a = Card(self.RANK_ALLOWED_VALUES[i], s)
                b = Card(self.RANK_ALLOWED_VALUES[i + 1], s)
                self.assertTrue(b > a)

    def test_lt(self):
        for r in Rank.ALLOWED_VALUES:
            for s in Suit.ALLOWED_VALUES:
                a = Card(r, s)
                b = Card(r, s)

                self.assertFalse(a < b)
                self.assertFalse(b < a)

        for r in Rank.ALLOWED_VALUES:  # Same rank with different suit should be equal
            for i in range(len(Suit.ALLOWED_VALUES) - 1):
                a = Card(r, Suit.ALLOWED_VALUES[i])
                b = Card(r, Suit.ALLOWED_VALUES[i + 1])
                self.assertFalse(a < b)
                self.assertFalse(b < a)

        for i in range(len(self.RANK_ALLOWED_VALUES) - 1):  # Different rank with same suit should not be equal
            for s in Suit.ALLOWED_VALUES:
                a = Card(self.RANK_ALLOWED_VALUES[i], s)
                b = Card(self.RANK_ALLOWED_VALUES[i + 1], s)
                self.assertLess(a, b)

    def test_unique_hash(self):
        d = {}
        for r in self.RANK_ALLOWED_VALUES:
            for s in Suit.ALLOWED_VALUES:
                c = Card(r, s)
                d[c] = c

        self.assertEqual(len(d), len(self.RANK_ALLOWED_VALUES) * len(Suit.ALLOWED_VALUES))

        for r in self.RANK_ALLOWED_VALUES:
            for s in Suit.ALLOWED_VALUES:
                c = Card(r, s)
                self.assertEqual(c, d[c])
