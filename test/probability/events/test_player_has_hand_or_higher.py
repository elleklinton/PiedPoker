from unittest import TestCase

from card_internals.card import Card
from hands.flush import Flush
from hands.four_of_a_kind import FourOfAKind
from hands.full_house import FullHouse
from hands.royal_flush import RoyalFlush
from hands.straight import Straight
from hands.straight_flush import StraightFlush
from hands.three_of_a_kind import ThreeOfAKind
from probability.events.player_has_hand_or_higher import PlayerHasHandOrHigher
from test.probability.events.events_test_utils import EventsTestUtils


class TestPlayerHasHandOrHigher(TestCase):
    def test_is_event(self):
        p1_cards = [Card('as'), Card('kd')]
        community_cards = [Card('ad'), Card('ac'), Card('ks')]

        EventsTestUtils.assert_is_event(self, PlayerHasHandOrHigher(FullHouse), player_1_cards=p1_cards,
                                        community_cards=community_cards)
        EventsTestUtils.assert_is_event(self, PlayerHasHandOrHigher(ThreeOfAKind), player_1_cards=p1_cards,
                                        community_cards=community_cards)
        EventsTestUtils.assert_is_event(self, PlayerHasHandOrHigher(Straight), player_1_cards=p1_cards,
                                        community_cards=community_cards)
        EventsTestUtils.assert_is_event(self, PlayerHasHandOrHigher(Flush), player_1_cards=p1_cards,
                                        community_cards=community_cards)

    def test_is_not_event(self):
        p1_cards = [Card('as'), Card('kd')]
        community_cards = [Card('ad'), Card('ac'), Card('ks')]

        EventsTestUtils.assert_is_not_event(self, PlayerHasHandOrHigher(FourOfAKind), player_1_cards=p1_cards,
                                            community_cards=community_cards)
        EventsTestUtils.assert_is_not_event(self, PlayerHasHandOrHigher(StraightFlush), player_1_cards=p1_cards,
                                            community_cards=community_cards)
        EventsTestUtils.assert_is_not_event(self, PlayerHasHandOrHigher(RoyalFlush), player_1_cards=p1_cards,
                                            community_cards=community_cards)
