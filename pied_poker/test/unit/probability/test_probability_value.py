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
        self.assertEqual(pv.__odds_str__, '2.0:1 odds')

    def test_ratio_str(self):
        pv = ProbabilityValue(1, 2)
        self.assertEqual(pv.__ratio_str__, '1/2')

    def test_str(self):
        pv = ProbabilityValue(1, 2)
        self.assertEqual(str(pv), '50.0% == 1:1.0 odds == (1/2)')

    def test_event_count_greater_than_given_count(self):
        try:
            pv = ProbabilityValue(4, 2)
            self.fail('Error: expected to throw invalid ProbabityValue')
        except RuntimeError as e:
            self.assertEqual(str(e), 'Error: event_count (4) cannot be greater than given_count (2).')

    def test_zero_event_count(self):
        pv = ProbabilityValue(0, 2)
        self.assertEqual(str(pv), '0.0% == 1:infinity odds == (0/2)')

    def test_zero_given_count(self):
        pv = ProbabilityValue(0, 0)
        self.assertEqual(str(pv), '0.0% == 1:infinity odds == (0/0)')

    def test_100_probability(self):
        pv = ProbabilityValue(100, 100)
        self.assertEqual(str(pv), '100.0% == infinity:1 odds == (100/100)')

    def test_margin_of_error(self):
        pv = ProbabilityValue(1, 2)
        self.assertEqual(0.692951912174839, pv.margin_of_error())

        pv = ProbabilityValue(50, 100)
        self.assertEqual(0.0979981992270027, pv.margin_of_error())

        pv = ProbabilityValue(50, 100)
        self.assertEqual(0.12879146517744502, pv.margin_of_error(0.99))

        pv = ProbabilityValue(90, 100)
        self.assertEqual(0.058798919536201616, pv.margin_of_error())

        pv = ProbabilityValue(100, 100)
        self.assertEqual(0, pv.margin_of_error())
