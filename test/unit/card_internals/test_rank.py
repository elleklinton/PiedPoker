from unittest import TestCase

from card_internals.rank import Rank


class TestRank(TestCase):
    RANK_ALLOWED_VALUES = [v for v in Rank.ALLOWED_VALUES if v != 't']

    def test_init_sad(self):
        try:
            Rank('1')
        except AssertionError as e:
            e: AssertionError
            self.assertEqual(len(e.args), 1)
            self.assertEqual(e.args[0], 'Invalid Value: 1')

    def test_init_happy(self):
        for r in Rank.ALLOWED_VALUES:
            Rank(r)
            if r.isdigit():
                Rank(int(r))

    def test_eq(self):
        for r in Rank.ALLOWED_VALUES:
            a = Rank(r)
            b = Rank(r)
            self.assertEqual(a, b)

    def test_gt(self):
        for i in range(len(self.RANK_ALLOWED_VALUES) - 1):
            a = Rank(self.RANK_ALLOWED_VALUES[i])
            b = Rank(self.RANK_ALLOWED_VALUES[i + 1])
            self.assertNotEqual(a, b)
            self.assertGreater(b, a)

    def test_lt(self):
        for i in range(len(self.RANK_ALLOWED_VALUES) - 1):
            a = Rank(self.RANK_ALLOWED_VALUES[i])
            b = Rank(self.RANK_ALLOWED_VALUES[i + 1])
            self.assertNotEqual(a, b)
            self.assertLess(a, b)

    def test_unique_hash(self):
        d = {}
        for r in self.RANK_ALLOWED_VALUES:
            a = Rank(r)
            d[a] = a

        self.assertEqual(len(d), len(self.RANK_ALLOWED_VALUES))

        for r in Rank.ALLOWED_VALUES:
            self.assertEqual(Rank(r), d[Rank(r)])

    def test_str(self):
        r = Rank("2")
        self.assertEqual(r.__str__(), '2')
        self.assertEqual(r.__repr__(), '2')

    def test_sub(self):
        self.assertEqual(Rank(10) - Rank(8), 2)
        self.assertEqual(Rank(10) - 2, 8)
        self.assertEqual(Rank(2) - Rank('a'), 1)

    def test_add(self):
        self.assertEqual(Rank(2) + Rank(3), 5)
        self.assertEqual(Rank(5) + 2, 7)


