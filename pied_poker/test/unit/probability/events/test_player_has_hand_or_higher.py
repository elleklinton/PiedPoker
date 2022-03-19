from unittest import TestCase

from pied_poker.card.card import Card
from pied_poker.hand.flush import Flush
from pied_poker.hand import FourOfAKind
from pied_poker.hand import FullHouse
from pied_poker.hand import RoyalFlush
from pied_poker.hand import Straight
from pied_poker.hand import StraightFlush
from pied_poker.hand import ThreeOfAKind
from pied_poker.probability.events.player_has_hand_or_higher import PlayerHasHandOrHigher
from pied_poker.test.unit.probability.events.events_test_utils import EventsTestUtils


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
        community_cards = [Card('ad'), Card('ac'), Card('ks'), Card('10s'), Card('5d')]

        EventsTestUtils.assert_is_not_event(self, PlayerHasHandOrHigher(FourOfAKind), player_1_cards=p1_cards,
                                            community_cards=community_cards)
        EventsTestUtils.assert_is_not_event(self, PlayerHasHandOrHigher(StraightFlush), player_1_cards=p1_cards,
                                            community_cards=community_cards)
        EventsTestUtils.assert_is_not_event(self, PlayerHasHandOrHigher(RoyalFlush), player_1_cards=p1_cards,
                                            community_cards=community_cards)
