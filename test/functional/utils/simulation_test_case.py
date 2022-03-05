from unittest import TestCase
import inspect

from player.player import Player
from probability.base_poker_event import BasePokerEvent
from round.native.round_simulator import RoundSimulator
from test.functional.utils.simulation_test_case_payload import SimulationTestCasePayload


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class SimulationTestCase(TestCase):
    def __assert_probability__(self, round_simulator: RoundSimulator, payload: SimulationTestCasePayload):
        """
        Asserts that with the given round_simulator, and the given target_event, the probability is within + or - delta
        of the target_probability

        :param round_simulator: The round simulator object to use
        :type round_simulator: RoundSimulator
        :param target_event: The target event to calculate probability for
        :type target_event: BasePokerEvent
        :param target_probability: The target probability that is expected
        :type target_probability: float
        :param n_rounds: The number of rounds to run the simulation for, default value 10,000
        :type n_rounds: int
        :param delta: The acceptable deviation from probability
        :type delta: float
        :param n_jobs: The number of jobs to use during parallelization
        :type n_jobs: int
        """

        result = round_simulator.simulate(payload.n_rounds, payload.n_jobs, False)

        payload.actual_probability = result.probability_of(payload.target_event, payload.given_event).probability
        msg = f'\n\n{self.current_function_name(3)}\n{payload}'

        self.assertAlmostEqual(payload.actual_probability, payload.target_probability,
                               delta=payload.delta,
                               msg=msg)

    def assert_probability(self, payload: SimulationTestCasePayload):
        """
        Asserts that in the given scenario, the probability is within the delta of the expected probability.

        :param payload: The payload for the functional test
        :type payload: SimulationTestCasePayload
        """
        player = Player('Ellek', cards=payload.player_cards)
        simulator = payload.simulator_factory_fn(payload.community_cards, [player], total_players=payload.n_players)

        self.__assert_probability__(simulator, payload)
        msg = f'{bcolors.OKGREEN}{self.current_function_name(2)}\n{payload}\n{" " * 5}PASSED\n'
        print(msg)

    def current_function_name(self, levels_up=1):
        return f'{inspect.stack()[levels_up][3]}'




