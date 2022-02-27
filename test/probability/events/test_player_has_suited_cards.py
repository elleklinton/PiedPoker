from unittest import TestCase

from card_internals.card import Card
from probability.events.player_has_suited_cards import PlayerHasSuitedCards
from test.probability.events.events_test_utils import EventsTestUtils


class TestPlayerHasSuitedCards(TestCase):
    def test_is_event(self):
        # Test not for suited connectors
        EventsTestUtils.assert_is_event(self, PlayerHasSuitedCards(), player_1_cards=[Card('5s'), Card('6s')])
        EventsTestUtils.assert_is_event(self, PlayerHasSuitedCards(), player_1_cards=[Card('as'), Card('2s')])

        # Test for suited connectors
        EventsTestUtils.assert_is_event(self, PlayerHasSuitedCards(only_suited_connectors=True),
                                        player_1_cards=[Card('5s'), Card('6s')])
        EventsTestUtils.assert_is_event(self, PlayerHasSuitedCards(only_suited_connectors=True),
                                        player_1_cards=[Card('as'), Card('2s')])
        EventsTestUtils.assert_is_event(self, PlayerHasSuitedCards(only_suited_connectors=True),
                                        player_1_cards=[Card('2s'), Card('as')])

    def test_is_not_event(self):
        # Don't test for suited connectors
        EventsTestUtils.assert_is_not_event(self, PlayerHasSuitedCards(), player_1_cards=[Card('5s'), Card('5d')])
        EventsTestUtils.assert_is_not_event(self, PlayerHasSuitedCards(), player_1_cards=[Card('5d'), Card('10s')])

        # Test for suited connectors
        EventsTestUtils.assert_is_not_event(self, PlayerHasSuitedCards(only_suited_connectors=True),
                                        player_1_cards=[Card('5s'), Card('7s')])
        EventsTestUtils.assert_is_not_event(self, PlayerHasSuitedCards(only_suited_connectors=True),
                                        player_1_cards=[Card('as'), Card('2d')])
        EventsTestUtils.assert_is_not_event(self, PlayerHasSuitedCards(only_suited_connectors=True),
                                        player_1_cards=[Card('2d'), Card('as')])
