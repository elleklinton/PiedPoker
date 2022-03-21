from unittest import TestCase

from pied_poker.probability.base_poker_event import BasePokerEvent


class TestBasePokerEvent(TestCase):
    def test_cannot_call_base_poker_event(self):
        try:
            BasePokerEvent().is_event(None)
            self.fail('Error: expected to throw')
        except NotImplementedError as e:
            self.assertEqual(str(e), 'Error: PokerEvent.is_event is undefined')