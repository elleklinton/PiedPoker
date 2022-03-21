from typing import List
from statistics import NormalDist

from pied_poker.card.card import Card
from pied_poker.probability.base_poker_event import BasePokerEvent
from pied_poker.test.functional.utils.simulator_factory import SimulatorFactory


class SimulationTestCasePayload:
    def __init__(self, simulator_factory_fn: SimulatorFactory.SIGNATURE, community_cards: List[Card],
                 player_cards: List[Card], target_event: BasePokerEvent, target_probability: float, delta: float = 0.01,
                 n_jobs: int = -1, given_event: BasePokerEvent = None, n_players: int = 1):
        """
        A class to store the payload of a functional test case.

        :param simulator_factory_fn: The function to generate the round simulator object
        :type simulator_factory_fn: SimulatorFactory.SIGNATURE
        :param community_cards: The community cards
        :type community_cards: List[Card]
        :param player_cards: The player cards
        :type player_cards: List[Card]
        :param target_event: The target event to calculate
        :type target_event: BasePokerEvent
        :param target_probability: The expected probability
        :type target_probability: float
        :param delta: The acceptable deviation from probability
        :type delta: float
        :param n_jobs: The number of jobs to use during parallelization
        :type n_jobs: int
        :param given_event: The given space to calculate the event in
        :type given_event: BasePokerEvent
        :param n_players: The number of players
        :type n_players: int
        """

        self.simulator_factory_fn = simulator_factory_fn
        self.community_cards = community_cards
        self.player_cards = player_cards
        self.target_event = target_event
        self.target_probability = target_probability
        self.actual_probability: float = -1
        self.delta = delta
        self.n_rounds = self.__n_rounds_needed__(target_probability, delta, 0.999)
        self.n_jobs = n_jobs
        self.given_event = given_event
        self.n_players = n_players

    @staticmethod
    def __n_rounds_needed__(target_probability: float, acceptable_delta: float, confidence: float = 0.999):
        """
        Calculates the number of rounds needed to get within delta of the target_probability, with the desired
        confidence level (default 99.9%) using Cochran's formula.
        :param target_probability: The true probability we are trying to calculate
        :type target_probability: float
        :param acceptable_delta: The acceptable deviation from target_probability we are willing to accept
        :type acceptable_delta: float
        :param confidence: The level of confidence we want in our sample. E.g. if confidence is 0.99 = 99%, then in
        99% of our samples, we would see the measured value within delta of the true value.
        :type confidence: float

        :return: Number of samples needed to achieve the desired results
        :rtype: int
        """

        z_score = NormalDist().inv_cdf((1 + confidence) / 2)
        n = (z_score**2 * target_probability * (1 - target_probability)) / (acceptable_delta ** 2)
        return round(n)


    def __str__(self):
        s = ' ' * 5
        actual_delta = abs(self.target_probability - self.actual_probability)

        return f'P({self.target_event} | {self.given_event}):' \
               f'\n{s}(n = {self.n_rounds})' \
               f'\n{s}Player Cards: {self.player_cards}' \
               f'\n{s}Community Cards: {self.community_cards}' \
               f'\n{s}Expected: {round(self.target_probability, 3)}' \
               f'\n{s}Actual: {round(self.actual_probability, 3)}' \
               f'\n{s}Delta: {round(actual_delta, 3)} (tolerance {round(self.delta, 3)})'

    def __repr__(self):
        return str(self)
