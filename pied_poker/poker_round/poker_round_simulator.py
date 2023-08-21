from __future__ import annotations

import sys
from typing import List, Callable
from joblib import Parallel, delayed
from tqdm import tqdm
from copy import deepcopy

import pied_poker.card.card as card
import pied_poker.player.player as player
import pied_poker.poker_round.poker_round_simulation_result as simulation_probability
import pied_poker.poker_round.poker_round as round
import pied_poker.poker_round.poker_round_result as round_result


class PokerRoundSimulator:
    def __init__(self, community_cards: List[card.Card] = (), players: List[player.Player] = (), total_players: int = 5,
                 other_drawn_cards: List[card.Card] = ()):
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
            i = i + 1 + len(players)
            players.append(player.Player(f'player_{i}', []))

        self.round = round.PokerRound(community_cards, players, other_drawn_cards)
        self.players = self.round.players

    def simulate(self, n: int = 1000,
                 n_jobs: int = -1,
                 status_bar: bool = True,
                 callback: Callable[[float], None] = lambda x: None,
                 callback_frequency: float = 0.01) -> simulation_probability.PokerRoundSimulationResult:
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
        :param callback: Called on progress intervals. Only called when n_jobs is 1 (no parallelization)
        :type: Callable[[float], None]
        :param callback_frequency: The frequency at which the callback is called, in percent. I.e. to call the callback
        every 1 percent of progress, set callback_frequency to 0.01. To call the callback every 0.05 percents of progress, set
        callback_frequency to 5.
        :type: float
        :return: SimulationProbability object, used to compute probabilities based on the simulations run.
        :rtype: SimulationProbability
        """
        simulations: List[round_result.PokerRoundResult]

        interactive_console = bool(getattr(sys, 'ps1', sys.flags.interactive))
        # If we are in interactive console, prevent threading because it breaks there

        if n_jobs == 1 or interactive_console:  # Don't want to parallelize
            if n_jobs != 1 and interactive_console:
                print(f'Warning: Threading was requested (n_jobs={n_jobs}), but disabling threading because interactive'
                      f' console was detected.')

            simulations = []
            rounds_per_callback = n * callback_frequency
            rounds_since_last_callback = rounds_per_callback - 1
            for i in range(n) if not status_bar else tqdm(range(n)):
                simulations.append(self.round.simulate())
                rounds_since_last_callback += 1
                if rounds_since_last_callback == rounds_per_callback:
                    callback(i / n)
                    rounds_since_last_callback = 0
        else:
            if not status_bar:
                simulations = Parallel(n_jobs=n_jobs)(delayed(self.round.simulate)() for i in range(n))
            else:
                simulations = Parallel(n_jobs=n_jobs)(delayed(self.round.simulate)() for i in tqdm(range(n)))

        callback(1)

        return simulation_probability.PokerRoundSimulationResult(simulations)
