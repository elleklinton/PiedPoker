from unittest import TestCase

from pied_poker.card.card import Card
from pied_poker.card.rank import Rank
from pied_poker.probability.events.player_has_card_ranks import PlayerHasCardRanks
from pied_poker.test.unit.probability.events.events_test_utils import EventsTestUtils


class TestPlayerHasCardRanks(TestCase):
    def test_is_event(self):
        p1_cards = [Card('as'), Card('kd')]

        EventsTestUtils.assert_is_event(self, PlayerHasCardRanks([Rank('a')]), player_1_cards=p1_cards)
        EventsTestUtils.assert_is_event(self, PlayerHasCardRanks([Rank('k')]), player_1_cards=p1_cards)
        EventsTestUtils.assert_is_event(self, PlayerHasCardRanks([Rank('k'), Rank('a')]), player_1_cards=p1_cards)

    def test_is_not_event(self):
        p1_cards = [Card('as'), Card('kd')]

        EventsTestUtils.assert_is_not_event(self, PlayerHasCardRanks([Rank('2')]), player_1_cards=p1_cards)
        EventsTestUtils.assert_is_not_event(self, PlayerHasCardRanks([Rank('a'), Rank('2')]), player_1_cards=p1_cards)
