from typing import List

from probability.base_poker_event import BasePokerEvent
from probability.probability_value import ProbabilityValue
from round.round_result import RoundResult


class SimulationProbability:
    def __init__(self, simulation_rounds: List[RoundResult]):
        """
        An object to store the results of a poker simulation and compute probabilities based on those events.
        :param simulation_rounds: A list of RoundResult objects
        :type simulation_rounds: RoundResult
        """
        self.__rounds__ = simulation_rounds

    def probability_of(self, event: BasePokerEvent, given: BasePokerEvent = None):
        """
        Used to compute the probability of a certain event occurring during the simulations.
        Example Usage:

        # Calculate probability of flush given suited cards
        SimulationProbability(..).probability_of(
            event=PlayerHasHand(Flush),
            given=PlayerHasSuitedCards()
        )

        # Calculate probability of 3 of a kind or higher given pocket pair
        SimulationProbability(..).probability_of(
            event=PlayerHasHandOrHigher(ThreeOfAKind),
            given=PlayerHasPocketPair()
        )

        :param event: The event you are looking for, see above example usage
        :type event: BasePokerEvent
        :param given: A "given", see above sample usage
        :type given: BasePokerEvent
        :return: The probability of the event occurring in the given space
        :rtype:
        """
        if not given:
            given_space = self.__rounds__
        else:
            given_space = [r for r in self.__rounds__ if given.filter_fn(r)]

        event_space = [r for r in given_space if event.filter_fn(r)]

        return ProbabilityValue(len(event_space), len(given_space))
