from typing import List
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import math
import scipy.stats as st
from matplotlib.ticker import FixedLocator

from pied_poker.probability.probability_value import ProbabilityValue
from pied_poker.card.card import Card
from pied_poker.player.player import Player
from pied_poker.poker_round.poker_round_simulator import PokerRoundSimulator
from pied_poker.probability.events.player_wins import PlayerWins


class DataGenerator:
    def __init__(self, left_dimension: str, bottom_dimension: str, strength_dimension: str = 'strength',
                 strength_label: str = 'Strength'):
        """
        Generates data for a heatmap.
        :param left_dimension: Left dimension of the heatmap
        :type left_dimension: str
        :param bottom_dimension: Bottom dimension of the heatmap
        :type bottom_dimension: str
        :param strength_dimension: Strength dimension of the heatmap
        :type bottom_dimension: str
        :param strength_label: Strength label of the heatmap
        :type strength_label: str
        """
        self.left_dimension = left_dimension
        self.bottom_dimension = bottom_dimension
        self.strength_dimension = strength_dimension
        self.strength_label = strength_label

    @staticmethod
    def win_probability(starting_cards, n=5000, total_players=2) -> ProbabilityValue:
        """
        Returns the probability that the player wins, given the starting cards, number of simulations, and total players
         at the table.
        :param starting_cards: Starting cards for the player
        :type starting_cards: List[Card]
        :param n: Number of simulations to run
        :type n: int
        :param total_players: Number of total players at the table
        :type total_players: int
        :return: Probability of winning (i.e. 0.85 for AA)
        :rtype: ProbabilityValue
        """
        # First, create our player with the starting cards
        player = Player('me', starting_cards)
        # Then, initialize our round simulator with NO community cards, and 2 total players
        round_simulator = PokerRoundSimulator(community_cards=[], players=[player], total_players=total_players)
        # Run the simulation n times
        simulation_result = round_simulator.simulate(n, n_jobs=1, status_bar=False)
        # Return the probability that player wins.
        return simulation_result.probability_of(PlayerWins())

    @staticmethod
    def margin_of_error(probability_value: float, sample_size: int, confidence_level=0.95):
        """
        Returns the margin of error for a given probability value and sample size.
        :param probability_value: The probability value
        :type probability_value: float
        :param sample_size: The sample size
        :type sample_size: int
        :param confidence_level: The confidence level (default 0.95)
        :type confidence_level: float
        :return: The margin of error
        :rtype: float
        """
        if probability_value == 0 or probability_value == 1:
            return 0

        z = st.norm.ppf(1 - (1 - confidence_level) / 2)
        return z * math.sqrt(probability_value * (1 - probability_value) / sample_size)

    def max_margin_of_error(self, df, n_rounds):
        """
        Calculates the max margin of error for the given dataframe and number of rounds.
        :param df: The dataframe with the simulation results
        :type df: pd.DataFrame
        :param n_rounds: Number of rounds
        :type n_rounds: int
        :return: Margin of error
        :rtype: float
        """
        # Find the value closest to 50, which will have max margin of error
        how_far_from_50 = df[self.strength_dimension].sub(50).abs().min()
        closest_value_to_50 = 50 + how_far_from_50
        highest_moe = self.margin_of_error(closest_value_to_50 / 100, n_rounds)

        return highest_moe

    def generate(self, n_rounds: int = 1000, n_players=2, n_jobs=1) -> pd.DataFrame:
        """
        Generates the data for the heatmap. Generates a heatmap with a column self.left_dimension, a column
        self.bottom_dimension, and a column self.strength_dimension.

        :param n_rounds: Number of rounds to simulate
        :type n_rounds: int
        :param n_players: Number of players at the table
        :type n_players: int
        :param n_jobs: Number of jobs to run in parallel. -1 means all processors.
        :type n_jobs: int
        :return:
        :rtype:
        """
        raise NotImplementedError('generate() must be implemented by a subclass of DataGenerator.')

    def sort_pivot(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Sorts the pivot table by the left dimension and bottom dimension.
        :param df: Pivot table
        :type df: pd.DataFrame
        :return:
        :rtype:
        """
        raise NotImplementedError('sort_pivot() must be implemented by a subclass of DataGenerator.')

    def visualize(self, df, title, n_rounds, x_ticks_suffix='', y_ticks_suffix='', n_jobs=1):
        """
        Visualizes the data.
        :param y_ticks_suffix: Suffix for y-axis tick labels
        :type y_ticks_suffix: str
        :param x_ticks_suffix: Suffix for x-axis tick labels
        :type x_ticks_suffix: str
        :param n_rounds: Number of rounds to simulate
        :type n_rounds: int
        :param df: Dataframe to visualize. Should have three columns: left_dimension, bottom_dimension, and
        strength_dimension.
        :type df: pd.DataFrame
        :param title: Title of the heatmap
        :type title: str
        :param n_jobs: Number of jobs to run in parallel. -1 means all processors.
        :type n_jobs: int
        :return:
        :rtype:
        """

        # Pivot the DataFrame for the heatmap
        poker_hands_pivot = df.pivot(index=self.left_dimension, columns=self.bottom_dimension, values=self.strength_dimension)

        # Sort the pivot table
        poker_hands_pivot = self.sort_pivot(poker_hands_pivot)

        y_len = len(poker_hands_pivot.index)
        x_len = len(poker_hands_pivot.columns)

        # Calculating the positions for the tick labels to be centered in each box
        x_centered_ticks = np.arange(x_len) + 0.5
        y_centered_ticks = np.arange(y_len) + 0.5

        # Create the heatmap with specified modifications
        plt.figure(figsize=(10, 8))
        ax = sns.heatmap(poker_hands_pivot,
                         annot=True,
                         fmt=".1f",
                         cmap='RdYlGn',
                         cbar_kws={'label': self.strength_label},
                         vmin=0,
                         vmax=100
                         )
        plt.title(title, fontsize=15, weight="medium")
        plt.xlabel("")  # Remove x-axis label
        plt.ylabel("")  # Remove y-axis label

        # Set the font size for the tick labels
        ax.figure.axes[-1].yaxis.label.set_size(15)
        cbar = ax.collections[0].colorbar
        cbar.ax.tick_params(labelsize=15)

        # Set the cbar labels to have % appended
        cbar.set_ticks(FixedLocator([0, 20, 40, 60, 80, 100]))
        cbar.set_ticklabels(['0%', '20%', '40%', '60%', '80%', '100%'])

        # Set the tick labels to be centered in each box and aligned on both axes
        plt.xticks(ticks=x_centered_ticks, fontsize=20)
        plt.yticks(ticks=y_centered_ticks, rotation=0, fontsize=20)  # Reverse the order of y-axis labels

        # Remove the tick lines for a cleaner look
        plt.tick_params(length=0)

        # Append the suffixes to the tick labels
        x_tick_labels = [label.get_text() + x_ticks_suffix for label in plt.gca().get_xticklabels()]
        y_tick_labels = [label.get_text() + y_ticks_suffix for label in plt.gca().get_yticklabels()]
        plt.gca().set_xticklabels(x_tick_labels)
        plt.gca().set_yticklabels(y_tick_labels)

        # Populate the bottom text
        highest_moe = self.max_margin_of_error(df, n_rounds)
        bottom_txt = f"\nMargin of Error: ±{round(highest_moe * 100, 1)}%"
        bottom_txt += f"\nSource: Ellek Linton via Pied Poker\n"
        plt.xlabel(bottom_txt, fontsize=15, fontstyle='italic')
        plt.subplots_adjust(bottom=0.15)
