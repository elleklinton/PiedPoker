from typing import List
from unittest import TestCase

from pied_poker.card.card import Card
from pied_poker.player import Player
from pied_poker.probability.base_poker_event import BasePokerEvent
from pied_poker.poker_round import PokerRound


class EventsTestUtils:
    @staticmethod
    def build_round_result(player_1_cards: List[Card]=(), player_2_cards: List[Card]=(), community_cards: List[Card]=()):
        p1 = Player('p1', player_1_cards)
        p2 = Player('p2', player_2_cards)
        return PokerRound(community_cards, [p1, p2]).simulate()

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