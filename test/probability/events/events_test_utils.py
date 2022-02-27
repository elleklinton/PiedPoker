from typing import List
from unittest import TestCase

from card_internals.card import Card
from player.player import Player
from probability.base_poker_event import BasePokerEvent
from round.round import Round


class EventsTestUtils:
    @staticmethod
    def build_round_result(player_1_cards: List[Card]=(), player_2_cards: List[Card]=(), community_cards: List[Card]=()):
        p1 = Player('p1', player_1_cards)
        p2 = Player('p2', player_2_cards)
        return Round(community_cards, [p1, p2]).simulate()

    @staticmethod
    def assert_is_event(test_instance: TestCase, event: BasePokerEvent, player_1_cards: List[Card] = (),
                        player_2_cards: List[Card] = (), community_cards: List[Card] = ()):
        r = EventsTestUtils.build_round_result(player_1_cards, player_2_cards, community_cards)
        test_instance.assertTrue(event.is_event(r), f'Error: expected RoundResult to be event {event.__class__.__name__}')

    @staticmethod
    def assert_is_not_event(test_instance: TestCase, event: BasePokerEvent, player_1_cards: List[Card] = (),
                        player_2_cards: List[Card] = (), community_cards: List[Card] = ()):
        r = EventsTestUtils.build_round_result(player_1_cards, player_2_cards, community_cards)
        test_instance.assertFalse(event.is_event(r), f'Error: expected RoundResult NOT to be event {event.__class__.__name__}')