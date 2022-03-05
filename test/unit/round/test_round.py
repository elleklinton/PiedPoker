from typing import List
from unittest import TestCase
import numpy as np
import random

from card_internals.card import Card
from deck_internals.deck import Deck
from player.player import Player
from round.round import Round


class TestRound(TestCase):
    def setUp(self) -> None:
        np.random.seed(420)
        random.seed(420)

    def test_single_deal_cards_helper(self, players: List[Player] = (), r: Round = None):
        if not r:
            r = Round(players=players)

        r.deal_cards()
        for p in r.players:
            self.assertEqual(len(p.cards), 2, f'Expected 2 cards to be dealt to {p.name}')

        self.assertEqual(len(set([c for p in r.players for c in p.cards])), len(r.players) * 2, 'Expected 2 cards to be'
                                                                                                ' dealt to each player')
        return r

    def test_deal_cards(self):
        for i in range(100):
            # Makes sure cards are dealt to all players
            p1 = Player('Ellek')
            p2 = Player('Snoop')
            self.test_single_deal_cards_helper([p1, p2])

            # Makes sure if a player already has cards, those cards are preserved
            p1 = Player('Ellek', cards=[Card('as'), Card('ad')])
            p2 = Player('Snoop')
            self.test_single_deal_cards_helper([p1, p2])
            self.assertEqual(p1.cards, [Card('as'), Card('ad')], 'Expected p1 cards to be unchanged')

    @staticmethod
    def __test_simulate_helper__(i):
        p1 = Player('Ellek', cards=[Card('as'), Card('ad')])
        p2 = Player('Snoop')
        deck = Deck(excluding=[Card('as'), Card('ad')])
        # Randomly draw between 0 and 5 community cards before round simulation
        community_cards = deck.draw(i % 5)

        # Randomly set between 0 and 10 cards to be already drawn (e.g. dealt to players who folded)
        already_drawn_cards = deck.draw((i % 10))

        r = Round(players=[p1, p2], community_cards=community_cards, other_drawn_cards=already_drawn_cards)

        return p1, p2, deck, community_cards, already_drawn_cards, r

    def test_starting_states_correct(self):
        for i in range(100):
            p1, p2, deck, community_cards, already_drawn_cards, r = self.__test_simulate_helper__(i)

            self.assertEqual(r.__starting_community_cards_state__, community_cards)
            self.assertEqual(r.__starting_deck_state__, deck)

    def test_simulate_all_players_dealt_two_cards(self):
        for i in range(100):
            p1, p2, deck, community_cards, already_drawn_cards, r = self.__test_simulate_helper__(i)
            result = r.simulate()

            self.assertEqual(result.player_during_round[p1].cards, [Card('as'), Card('ad')])
            self.assertEqual(len(result.player_during_round[p2].cards), 2)

    def test_simulate_5_community_cards_drawn(self):
        for i in range(100):
            p1, p2, deck, community_cards, already_drawn_cards, r = self.__test_simulate_helper__(i)
            result = r.simulate()

            self.assertEqual(len(result.community_cards), 5)

    def test_simulate_no_repeat_cards(self):
        # This tests that none of the already drawn cards are in community cards or dealt to other players
        for i in range(100):
            p1, p2, deck, community_cards, already_drawn_cards, r = self.__test_simulate_helper__(i)
            result = r.simulate()

            player_cards_dealt = [c for p in result.player_during_round.values() for c in p.cards]

            intersection = set(player_cards_dealt).intersection(set(already_drawn_cards))
            self.assertEqual(len(intersection), 0, f'Error: expected no overlap between player_cards_dealt '
                                                   f'({player_cards_dealt}) and already_drawn_cards '
                                                   f'({already_drawn_cards}) but found intersection {intersection}')

            intersection = set(player_cards_dealt).intersection(set(community_cards))
            self.assertEqual(len(intersection), 0, f'Error: expected no overlap between player_cards_dealt '
                                                   f'({player_cards_dealt}) and community_cards '
                                                   f'({community_cards}) but found intersection {intersection}')

            intersection = set(community_cards).intersection(set(already_drawn_cards))
            self.assertEqual(len(intersection), 0, f'Error: expected no overlap between community_cards '
                                                   f'({community_cards}) and already_drawn_cards '
                                                   f'({already_drawn_cards}) but found intersection {intersection}')

    def test_simulate_resets_to_default_state(self):
        for i in range(100):
            p1, p2, deck, community_cards, already_drawn_cards, r = self.__test_simulate_helper__(i)
            result = r.simulate()

            # Test player cards are reset to default state
            self.assertEqual(r.players[0].cards, [Card('as'), Card('ad')], f'Error: expected p1 cards to be reset to '
                                                                           f'same cards but got {r.players[0].cards}.')
            self.assertEqual(r.players[1].cards, [], f'Error: expected p0 cards to be reset to [] but got '
                                                     f'{r.players[1].cards}.')

            # Test community cards are reset to default state
            self.assertEqual(set(community_cards), set(r.community_cards), f'Error: expected community cards in reset '
                                                                           f'round ({r.community_cards}) to match '
                                                                           f'original state ({community_cards}).')

            # Test already drawn cards are preserved
            self.assertEqual(set(already_drawn_cards), set(r.other_drawn_cards), f'Error: expected already_drawn_cards '
                                                                           f'({already_drawn_cards}) to match '
                                                                           f'r.other_drawn_cards '
                                                                                 f'({r.other_drawn_cards}).')

    def test_round_str(self):
        p1 = Player('Ellek', cards=[Card('as'), Card('ad')])
        p2 = Player('Snoop')

        r = Round(players=[p1, p2])
        self.assertEqual(str(r), 'Players: [Ellek: [A♠, A♦], Snoop: []], Community Cards: [], Other Drawn Cards: []')
