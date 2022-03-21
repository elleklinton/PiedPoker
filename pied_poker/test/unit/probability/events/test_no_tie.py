from unittest import TestCase

from pied_poker.card.card import Card
from pied_poker.probability.events.no_tie import NoTie
from pied_poker.test.unit.probability.events.events_test_utils import EventsTestUtils


class TestNoTie(TestCase):
    def test_is_event(self):

        p1_cards = [Card('7s'), Card('8s')]
        p2_cards = [Card('2s'), Card('3s')]
        community_cards = [Card('4s'), Card('5s'), Card('6s')]
        EventsTestUtils.assert_is_event(self, NoTie(), p1_cards, p2_cards, community_cards)

    def test_is_not_event(self):
        p1_cards = [Card('5s'), Card('5h')]
        p2_cards = [Card('5d'), Card('5c')]
        community_cards = [Card('4s'), Card('4d'), Card('4c'), Card('2s'), Card('2d')]
        EventsTestUtils.assert_is_not_event(self, NoTie(), p1_cards, p2_cards, community_cards)

        p1_cards = [Card('7s'), Card('8s')]
        p2_cards = [Card('7d'), Card('8d')]
        community_cards = [Card('4c'), Card('5c'), Card('6c')]
        EventsTestUtils.assert_is_not_event(self, NoTie(), p1_cards, p2_cards, community_cards)

