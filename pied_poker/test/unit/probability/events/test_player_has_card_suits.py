from unittest import TestCase

from pied_poker.card.card import Card
from pied_poker.card.suit import Suit
from pied_poker.probability.events.player_has_card_suits import PlayerHasCardSuits
from pied_poker.test.unit.probability.events.events_test_utils import EventsTestUtils


class TestPlayerHasCardSuits(TestCase):
    def test_is_event(self):
        p1_cards = [Card('as'), Card('kd')]

        EventsTestUtils.assert_is_event(self, PlayerHasCardSuits([Suit('s')]), player_1_cards=p1_cards)
        EventsTestUtils.assert_is_event(self, PlayerHasCardSuits([Suit('d')]), player_1_cards=p1_cards)
        EventsTestUtils.assert_is_event(self, PlayerHasCardSuits([Suit('d'), Suit('s')]), player_1_cards=p1_cards)

    def test_is_not_event(self):
        p1_cards = [Card('as'), Card('kd')]

        EventsTestUtils.assert_is_not_event(self, PlayerHasCardSuits([Suit('h')]), player_1_cards=p1_cards)
        EventsTestUtils.assert_is_not_event(self, PlayerHasCardSuits([Suit('c')]), player_1_cards=p1_cards)
        EventsTestUtils.assert_is_not_event(self, PlayerHasCardSuits([Suit('h'), Suit('s')]), player_1_cards=p1_cards)
