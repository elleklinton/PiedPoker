from unittest import TestCase

from pied_poker.card.card import Card
from pied_poker.probability.events import PlayerHasCards
from pied_poker.test.unit.probability.events.events_test_utils import EventsTestUtils


class TestPlayerHasCards(TestCase):
    def test_is_event(self):
        p1_cards = [Card('as'), Card('kd')]

        EventsTestUtils.assert_is_event(self, PlayerHasCards([Card('as')]), player_1_cards=p1_cards)
        EventsTestUtils.assert_is_event(self, PlayerHasCards([Card('kd')]), player_1_cards=p1_cards)
        EventsTestUtils.assert_is_event(self, PlayerHasCards([Card('kd'), Card('as')]), player_1_cards=p1_cards)

    def test_is_not_event(self):
        p1_cards = [Card('as'), Card('kd')]

        EventsTestUtils.assert_is_not_event(self, PlayerHasCards([Card('ac')]), player_1_cards=p1_cards)
        EventsTestUtils.assert_is_not_event(self, PlayerHasCards([Card('kc')]), player_1_cards=p1_cards)
        EventsTestUtils.assert_is_not_event(self, PlayerHasCards([Card('kc'), Card('kd')]), player_1_cards=p1_cards)
        EventsTestUtils.assert_is_not_event(self, PlayerHasCards([Card('kd'), Card('as'), Card('ad')]),
                                            player_1_cards=p1_cards)
        EventsTestUtils.assert_is_not_event(self, PlayerHasCards([Card('kd'), Card('as'), Card('2d')]),
                                            player_1_cards=p1_cards)
