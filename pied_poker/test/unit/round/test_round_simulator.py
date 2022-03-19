from unittest import TestCase
import numpy as np
import random

from pied_poker.card.card import Card
from pied_poker import Player
from pied_poker import RoundSimulator


class TestRoundSimulator(TestCase):
    def setUp(self) -> None:
        np.random.seed(420)
        random.seed(420)

    def test_auto_generate_remaining_players(self):
        players = [Player('Ellek'), Player('Snoop')]
        rs = RoundSimulator(players=players, total_players=9)
        self.assertEqual(len(rs.players), 9, f'Error: expected 9 players but got {len(rs.players)}')

        rs = RoundSimulator(players=players, total_players=2)
        self.assertEqual(len(rs.players), 2, f'Error: expected 2 players but got {len(rs.players)}')

    def test_community_cards_change_between_simulations(self):
        players = [Player('Ellek'), Player('Snoop')]
        rs = RoundSimulator(players=players, total_players=2)
        simulation_result = rs.simulate(50, 1, False)
        community_cards = set([tuple(r.community_cards) for r in simulation_result.__rounds__])
        # assert at least 45 unique community card sets
        self.assertGreaterEqual(len(community_cards), 45, f'Error: Expected > 45 unique community card sets, but got'
                                                          f' {len(community_cards)}')

    def test_player_dealt_cards_change_between_simulations(self):
        p1_cards = [Card('as'), Card('ad')]
        players = [Player('Ellek', cards=p1_cards), Player('Snoop')]
        rs = RoundSimulator(players=players, total_players=2)
        simulation_result = rs.simulate(50, 1, False)

        player_1_cards = [tuple(r.player_during_round[Player('Ellek')].cards) for r in simulation_result.__rounds__]
        player_2_cards = [tuple(r.player_during_round[Player('Snoop')].cards) for r in simulation_result.__rounds__]

        # assert at least 45 unique cards dealt to p2
        self.assertGreaterEqual(len(set(player_2_cards)), 45, f'Error: Expected > 45 unique card sets dealt to p2, but'
                                                              f' got {len(set(player_2_cards))}')
        # assert 1 set of cards dealt to p1 (since their cards were already pre-defined
        self.assertEqual(len(set(player_1_cards)), 1, f'Error: Expected player 1 to have same cards each round, but got'
                                                              f' {len(set(player_2_cards))} unique sets of cards dealt')

    def test_simulation_status_bar_options(self):
        # For code coverage to be complete, this has no practical effect
        rs = RoundSimulator(total_players=2)
        rs.simulate(0, 1, True)
        rs.simulate(0, 1, False)
        rs.simulate(0, 2, True)
        rs.simulate(0, 2, False)
