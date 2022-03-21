from typing import List, Dict
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

import pied_poker.probability.base_poker_event as base_poker_event
import pied_poker.probability.probability_value as probability_value
import pied_poker.poker_round.poker_round_result as round_result
import pied_poker.probability.events.player_has_hand as player_has_hand
import pied_poker.probability.events.player_wins as player_wins
import pied_poker.hand.poker_hand as poker_hand
import pied_poker.player as player


class PokerRoundSimulationResult:
    def __init__(self, simulation_rounds: List[round_result.PokerRoundResult]):
        """
        An object to store the results of a poker simulation and compute probabilities based on those events.
        :param simulation_rounds: A list of RoundResult objects
        :type simulation_rounds: RoundResult
        """
        self.__rounds__ = simulation_rounds

    def where(self, event: base_poker_event.BasePokerEvent):
        """
        Returns a new instance of PokerRoundSimulationResult, with only the results that match the event criteria

        :param event: The event you would like to filter by
        :type event: BasePokerEvent
        :return: List of PokerRoundResult objects that match the event criteria
        :rtype: List[base_poker_event.BasePokerEvent]
        """
        return PokerRoundSimulationResult([r for r in self.__rounds__ if event.filter_fn(r)])

    def sample(self):
        """
        Returns one random PokerRoundResult object from the events in the PokerRoundSimulationResult.
        :return: Returns one random PokerRoundResult object from the events in the PokerRoundSimulationResult.
        :rtype: PokerRoundResult
        """
        return np.random.choice(self.__rounds__, 1)[0]

    def probability_of(self, event: base_poker_event.BasePokerEvent, given: base_poker_event.BasePokerEvent = None)\
            -> probability_value.ProbabilityValue:
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

        return probability_value.ProbabilityValue(len(event_space), len(given_space))

    @staticmethod
    def __plot_barplot__(x: List[float], y: List[str], title: str):
        """
        An internal function to plot a barchart given a list of probabilities x and a list of labels y
        :param x: The list of probabilities
        :type x: List[float]
        :param y: The list of labels associated with each probability
        :type y: List[str]
        :param title: The title of the barchart
        :type title: str
        :return: None
        :rtype: None
        """
        sns.barplot(x=x, y=y, color='seagreen')
        plt.title(title)
        plt.show()

    def visualize_player_hand_distribution(self, player: player.Player = None):
        """
        Creates and shows a bar chart for the distribution of hands in the simulation.
        :param player: Optional, the player to visualize hands for. If blank, defaults to first player
        :type player: player.Player
        :return: None
        :rtype: None
        """
        hand_names = []
        hand_probabilities = []

        for hand_type in reversed(poker_hand.PokerHand.ALL_HANDS_RANKED):
            p = self.probability_of(player_has_hand.PlayerHasHand(hand_type, player))
            hand_names.append(hand_type.__name__ + f' ({p.__percent_str__})')
            hand_probabilities.append(p.probability)

        self.__plot_barplot__(hand_probabilities, hand_names, 'Hand Type Probabilities')

    def visualize_winner_distribution(self):
        """
        Creates and shows a bar chart for the distribution of winners in the simulation.
        :return: None
        :rtype: None
        """
        players = sorted(self.__rounds__[0].players_ranked, key=lambda p: p.name)
        player_names = []
        win_probabilities = []

        for player in players:
            p = self.probability_of(player_wins.PlayerWins(player))
            player_names.append(player.name + f' ({p.__percent_str__})')
            win_probabilities.append(p.probability)

        self.__plot_barplot__(win_probabilities, player_names, 'Probabilities of Winning')

    def visualize_winning_hands(self, cumulative: bool = True):
        """
        Creates and shows a bar chart for the distribution of winning hands in the simulation.
        :param cumulative: Whether to cumulate the percentages
        :type cumulative: bool
        :return: None
        :rtype: None
        """
        winning_hand_counts: Dict[str, int] = {}
        total_hands = 0

        for rnd in self.__rounds__:
            for winner in rnd.winners:
                winning_hand = winner.hand
                hand_str = winning_hand.__class__.__name__
                hand_count = winning_hand_counts.get(hand_str, 0) + 1
                winning_hand_counts[hand_str] = hand_count
                total_hands += 1

        hand_names = []
        hand_probabilities = []
        last_cumulative_probability = 0

        for hand_type in reversed(poker_hand.PokerHand.ALL_HANDS_RANKED):
            hand_str = hand_type.__name__
            hand_count = winning_hand_counts.get(hand_str, 0)
            if cumulative:
                hand_p = hand_count / (total_hands if total_hands > 0 else 1)
                hand_p += last_cumulative_probability
                last_cumulative_probability = hand_p
            else:
                hand_p = hand_count / (total_hands if total_hands > 0 else 1)
            hand_percent = f'{round(hand_p * 100, 2)}%'
            hand_names.append(hand_str + f' ({hand_percent})')
            hand_probabilities.append(hand_p)

        self.__plot_barplot__(hand_probabilities, hand_names, 'Distribution of Winning Hands')


