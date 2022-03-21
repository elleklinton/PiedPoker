from unittest import TestCase

from pied_poker.card.card import Card
from pied_poker.hand import FourOfAKind
from pied_poker.hand import FullHouse
from pied_poker.hand import ThreeOfAKind
from pied_poker.probability.events.player_has_hand import PlayerHasHand
from pied_poker.test.unit.probability.events.events_test_utils import EventsTestUtils


class TestPlayerHasHand(TestCase):
    def test_is_event(self):
        p1_cards = [Card('as'), Card('kd')]
        community_cards = [Card('ad'), Card('ac'), Card('ks'), Card('2d'), Card('3s')]

        EventsTestUtils.assert_is_event(self, PlayerHasHand(FullHouse), player_1_cards=p1_cards, community_cards=community_cards)
        EventsTestUtils.assert_is_event(self, PlayerHasHand([FullHouse, ThreeOfAKind]), player_1_cards=p1_cards,
                                        community_cards=community_cards)

    def test_is_not_event(self):
        p1_cards = [Card('as'), Card('kd')]
        community_cards = [Card('ad'), Card('ac'), Card('ks'), Card('2d'), Card('3s')]

        EventsTestUtils.assert_is_not_event(self, PlayerHasHand(ThreeOfAKind), player_1_cards=p1_cards, community_cards=community_cards)
        EventsTestUtils.assert_is_not_event(self, PlayerHasHand([FourOfAKind]), player_1_cards=p1_cards,
                                            community_cards=community_cards)
