from unittest import TestCase

from card_internals.suit import Suit


class TestSuit(TestCase):
    def test_init_sad(self):
        try:
            Suit('z')
        except AssertionError as e:
            e: AssertionError
            self.assertEqual(len(e.args), 1)
            self.assertEqual(e.args[0], 'Invalid Value: z')

    def test_init_happy(self):
        for r in Suit.ALLOWED_VALUES:
            Suit(r)

    def test_unique_hash(self):
        d = {}
        for r in Suit.ALLOWED_VALUES:
            a = Suit(r)
            d[a] = a

        self.assertEqual(len(d), len(Suit.ALLOWED_VALUES))

        for r in Suit.ALLOWED_VALUES:
            self.assertEqual(Suit(r), d[Suit(r)])

    def test_str(self):
        r = Suit("h")
        self.assertEqual(r.__str__(), '♥')
        self.assertEqual(r.__repr__(), '♥')
