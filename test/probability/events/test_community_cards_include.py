from unittest import TestCase

from card_internals.card import Card
from probability.events.community_cards_include import CommunityCardsInclude
from test.probability.events.events_test_utils import EventsTestUtils


class TestCommunityCardsInclude(TestCase):
    def test_is_event(self):
        community_cards = [Card('as'), Card('ad'), Card('ah'), Card('ac'), Card('10s')]

        EventsTestUtils.assert_is_event(self, CommunityCardsInclude([Card('as')]), community_cards=community_cards)
        EventsTestUtils.assert_is_event(self, CommunityCardsInclude([Card('as'), Card('ad')]),
                                        community_cards=community_cards)
        EventsTestUtils.assert_is_event(self, CommunityCardsInclude([Card('as'), Card('ad'), Card('ah')]),
                                        community_cards=community_cards)
        EventsTestUtils.assert_is_event(self, CommunityCardsInclude([Card('as'), Card('ad'), Card('ah'), Card('ac')]),
                                        community_cards=community_cards)
        EventsTestUtils.assert_is_event(self, CommunityCardsInclude([Card('as'), Card('ad'), Card('ah'), Card('ac'),
                                                                     Card('10s')]),
                                        community_cards=community_cards)

    def test_is_not_event(self):
        community_cards = [Card('as'), Card('ad'), Card('ah'), Card('ac'), Card('10s')]

        # doesn't include 6s
        EventsTestUtils.assert_is_not_event(self, CommunityCardsInclude([Card('as'), Card('ad'), Card('ah'), Card('ac'),
                                                                         Card('10s'), Card('6s')]),
                                            community_cards=community_cards)

        # doesn't include 6s
        EventsTestUtils.assert_is_not_event(self, CommunityCardsInclude([Card('6s')]),
                                            community_cards=community_cards)


