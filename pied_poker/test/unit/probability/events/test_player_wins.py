from unittest import TestCase

from pied_poker.card.card import Card
from pied_poker.player import Player
from pied_poker.probability.events.player_wins import PlayerWins
from pied_poker.test.unit.probability.events.events_test_utils import EventsTestUtils


class TestPlayerWins(TestCase):
    def test_is_event(self):
        p1_cards = [Card('5s'), Card('6s')]
        p2_cards = [Card('2s'), Card('3s')]
        community_cards = [Card('4s'), Card('7s'), Card('8s')]
        EventsTestUtils.assert_is_event(self, PlayerWins(includes_tie=False), p1_cards, p2_cards, community_cards)

        p1_cards = [Card('7s'), Card('8s')]
        p2_cards = [Card('2s'), Card('3s')]
        community_cards = [Card('4s'), Card('5s'), Card('6s')]
        EventsTestUtils.assert_is_event(self, PlayerWins(includes_tie=False), p1_cards, p2_cards, community_cards)

        p1_cards = [Card('7s'), Card('8s')]
        p2_cards = [Card('7d'), Card('8d')]
        community_cards = [Card('4c'), Card('5c'), Card('6c')]
        EventsTestUtils.assert_is_event(self, PlayerWins(includes_tie=True), p1_cards, p2_cards, community_cards)
        EventsTestUtils.assert_is_event(self, PlayerWins(includes_tie=True,
                                                         player=Player('p2')), p1_cards, p2_cards, community_cards)

    def test_is_not_event(self):
        p1_cards = [Card('2s'), Card('3s')]
        p2_cards = [Card('5s'), Card('6s')]
        community_cards = [Card('4s'), Card('7s'), Card('8s')]
        EventsTestUtils.assert_is_not_event(self, PlayerWins(includes_tie=False), p1_cards, p2_cards, community_cards)

        p1_cards = [Card('2s'), Card('3s')]
        p2_cards = [Card('7s'), Card('8s')]
        community_cards = [Card('4s'), Card('5s'), Card('6s')]
        EventsTestUtils.assert_is_not_event(self, PlayerWins(includes_tie=False), p1_cards, p2_cards, community_cards)
