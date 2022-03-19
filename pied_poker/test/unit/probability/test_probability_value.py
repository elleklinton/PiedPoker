from unittest import TestCase

from pied_poker.probability.probability_value import ProbabilityValue


class TestProbabilityValue(TestCase):
    def test_percent_str(self):
        pv = ProbabilityValue(1, 2)
        self.assertEqual(pv.__percent_str__, '50.0%')

    def test_odds_str(self):
        pv = ProbabilityValue(1, 3)
        self.assertEqual(pv.__odds_str__, '1:2.0 odds')

        pv = ProbabilityValue(2, 3)
        self.assertEqual(pv.__odds_str__, '1:0.5 odds')

    def test_ratio_str(self):
        pv = ProbabilityValue(1, 2)
        self.assertEqual(pv.__ratio_str__, '1/2')

    def test_str(self):
        pv = ProbabilityValue(1, 2)
        self.assertEqual(str(pv), '50.0% == 1:1.0 odds == (1/2)')
