from unittest import TestCase

from card_internals.card import Card
from card_internals.rank import Rank
from probability.events.player_has_pocket_pair import PlayerHasPocketPair
from test.unit.probability.events.events_test_utils import EventsTestUtils


class TestPlayerHasPocketPair(TestCase):
    def test_is_event(self):
        # Test general pocket pair
        EventsTestUtils.assert_is_event(self, PlayerHasPocketPair(), player_1_cards=[Card('5s'), Card('5d')])
        EventsTestUtils.assert_is_event(self, PlayerHasPocketPair(), player_1_cards=[Card('as'), Card('ad')])

        # Test exact_rank
        EventsTestUtils.assert_is_event(self, PlayerHasPocketPair(exact_rank=Rank('5')), player_1_cards=[Card('5s'),
                                                                                                         Card('5d')])
        EventsTestUtils.assert_is_event(self, PlayerHasPocketPair(exact_rank=Rank('a')), player_1_cards=[Card('as'),
                                                                                                         Card('ad')])

        # Test minimum_rank
        EventsTestUtils.assert_is_event(self, PlayerHasPocketPair(minimum_rank=Rank('5')),
                                        player_1_cards=[Card('5s'), Card('5d')])
        EventsTestUtils.assert_is_event(self, PlayerHasPocketPair(minimum_rank=Rank('5')),
                                        player_1_cards=[Card('as'), Card('ad')])

    def test_is_not_event(self):
        # Test general pocket pair without community card pair
        EventsTestUtils.assert_is_not_event(self, PlayerHasPocketPair(), player_1_cards=[Card('5s'), Card('6d')])
        EventsTestUtils.assert_is_not_event(self, PlayerHasPocketPair(), player_1_cards=[Card('as'), Card('kd')])
        EventsTestUtils.assert_is_not_event(self, PlayerHasPocketPair(), player_1_cards=[Card('5s'), Card('6d')],
                                            community_cards=[Card('6s'), Card('5d'), Card('5h')])

        # Test exact_rank
        EventsTestUtils.assert_is_not_event(self, PlayerHasPocketPair(exact_rank=Rank('6')),
                                            player_1_cards=[Card('5s'), Card('5d')])
        EventsTestUtils.assert_is_not_event(self, PlayerHasPocketPair(exact_rank=Rank('5')),
                                            player_1_cards=[Card('as'), Card('ad')])
        EventsTestUtils.assert_is_not_event(self, PlayerHasPocketPair(exact_rank=Rank('5')),
                                            player_1_cards=[Card('as'), Card('kd')])


        # Test minimum_rank
        EventsTestUtils.assert_is_not_event(self, PlayerHasPocketPair(minimum_rank=Rank('5')),
                                            player_1_cards=[Card('4s'), Card('4d')])
        EventsTestUtils.assert_is_not_event(self, PlayerHasPocketPair(minimum_rank=Rank('5')),
                                            player_1_cards=[Card('5s'), Card('ad')])
