from unittest import TestCase

from card_internals.card import Card
from hands.four_of_a_kind import FourOfAKind
from hands.full_house import FullHouse
from hands.three_of_a_kind import ThreeOfAKind
from probability.events.player_has_hand import PlayerHasHand
from test.probability.events.events_test_utils import EventsTestUtils


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
