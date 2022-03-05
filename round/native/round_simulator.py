from __future__ import annotations

from typing import List
from joblib import Parallel, delayed
from tqdm import tqdm
from copy import deepcopy

from card_internals.card import Card
from player.player import Player
from probability.simulation_probability import SimulationProbability
from round.native.round import Round
from round.native.round_result import RoundResult


class RoundSimulator:
    def __init__(self, community_cards: List[Card] = (), players: List[Player] = (), total_players: int = 5,
                 other_drawn_cards: List[Card] = ()):
        """
        Class used to simulate many poker rounds, given a current game state.
        Example Usage:
        p1 = Player('Ellek', [Card('as'), Card('ad')])
        simulator = RoundSimulator(community_cards=[], players=[p1], total_players=5)

        :param community_cards: A list of the community Card objects
        :type community_cards: List[Card]
        :param players: A list of the explicit players participating for whom hands are known.
        :type players: List[Player]
        :param total_players: The total number of players. This class will auto-generate the remaining players if
        len(players) < total_players. Default value 5.
        :type total_players: int
        """
        players = deepcopy(players) if players else []
        for i in range(total_players - len(players)):
            players.append(Player(f'player_{i}', []))

        self.round = Round(community_cards, players, other_drawn_cards)
        self.players = self.round.players

    def simulate(self, n: int = 1000, n_jobs: int = -1, status_bar: bool = True):
        """
        Runs a simulation of n poker games, and returns a SimulationProbability object, which is be used to compute
        probabilities based on the simulations run. This function is parallelized and configurable via function
        parameters.

        :param status_bar: Whether to display status bar
        :type status_bar: bool
        :param n: Number of simulations to run
        :type n: int
        :param n_jobs: Number of jobs used during process parallelization. To disable parallelization, set n_jobs to 1.
        To use all available CPUs, set n_jobs to -1. Do NOT use parallelization when running through an interactive
        console.
        :type n_jobs: int
        :return: SimulationProbability object, used to compute probabilities based on the simulations run.
        :rtype: SimulationProbability
        """
        simulations: List[RoundResult]

        if n_jobs == 1:  # Don't want to parallelize
            if not status_bar:
                simulations = [self.round.simulate() for i in range(n)]
            else:
                simulations = [self.round.simulate() for i in tqdm(range(n))]
        else:
            if not status_bar:
                simulations = Parallel(n_jobs=n_jobs)(delayed(self.round.simulate)() for i in range(n))
            else:
                simulations = Parallel(n_jobs=n_jobs)(delayed(self.round.simulate)() for i in tqdm(range(n)))

        return SimulationProbability(simulations)
