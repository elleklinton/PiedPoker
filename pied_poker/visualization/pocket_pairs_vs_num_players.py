from typing import List

import pandas as pd
from matplotlib import pyplot as plt

from pied_poker.visualization.data_generator import DataGenerator
from pied_poker.card.rank import Rank
from pied_poker.card.card import Card


class PocketPairsVsNumPlayers(DataGenerator):
    def __init__(self):
        """
        Generates data for all possible pocket pairs, pre-flop, compared against the number of players.
        """
        super().__init__(left_dimension='pocket_pair', bottom_dimension='num_players', strength_dimension='win_rate',
                         strength_label='Win Rate')

    @staticmethod
    def get_all_pocket_pairs() -> List[List[Card]]:
        """
        Returns a list of all possible pocket pairs.
        :return: A list of all possible pocket pairs
        :rtype: List[List[Card]]
        """
        all_starting_cards = []

        for rank in Rank.ALLOWED_VALUES:
            cards = Card.of(rank + 's', rank + 'c')
            all_starting_cards.append(cards)

        return all_starting_cards

    @staticmethod
    def label_for_pocker_pair(pocket_pair):
        # return str(pocket_pair[0].rank) + "'s"
        return ' '.join([str(p) for p in pocket_pair])

    def generate(self, n_rounds: int = 1000, min_players=2, max_players=9, n_jobs=1, print_progress=True) \
            -> pd.DataFrame:
        """
        Generates a dataframe with the probability of winning for each starting hand.
        :param print_progress: Whether to print progress
        :type print_progress: bool
        :param min_players: Minimum number of players at the table
        :type min_players: int
        :param max_players: Maximum number of players at the table
        :type max_players: int
        :param n_rounds: Number of rounds to simulate
        :type n_rounds: int
        :param n_jobs: Number of jobs to run in parallel. -1 means all processors.
        :type n_jobs: int
        :return:
        :rtype:
        """
        df = pd.DataFrame(columns=[self.left_dimension, self.bottom_dimension, self.strength_dimension])
        i = 0

        all_starting_cards = self.get_all_pocket_pairs()

        for pocket_pair in all_starting_cards:
            if print_progress:
                prog_pct = round(i * 100 / (len(all_starting_cards) * (max_players - min_players + 1)), 2)
                print(f'Calculating win probabilities for {self.label_for_pocker_pair(pocket_pair)} ({prog_pct}% done)')
            # Calculate win probability for each number of players
            for num_players in range(min_players, max_players + 1):
                p = self.win_probability(pocket_pair, n_rounds, total_players=num_players)
                # Add row to dataframe
                cards_as_str = self.label_for_pocker_pair(pocket_pair)
                df.loc[i] = [cards_as_str, num_players, p.probability * 100]
                i += 1

        df[self.bottom_dimension] = df[self.bottom_dimension].astype(str)

        return df

    def sort_pivot(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Sorts the pivot table by the left dimension and bottom dimension.
        :param df: The dataframe to sort
        :type df: pd.DataFrame
        :return: The sorted dataframe
        :rtype: pd.DataFrame
        """

        # Index is the left dimension, columns are the bottom dimension

        # First, sort the index dimension (left dimension)
        all_left_dimensions = [self.label_for_pocker_pair(pocket_pair) for pocket_pair in self.get_all_pocket_pairs()]
        # Reverse the index so that the highest card is at the top
        all_left_dimensions = all_left_dimensions[::-1]
        df.index = pd.CategoricalIndex(df.index, categories=all_left_dimensions)
        df.sort_index(level=0, inplace=True)

        return df

    def visualize(self, title=None, n_rounds=1000, min_players=2, max_players=9, n_jobs=1, print_progress=True):
        """
        Visualizes the data.
        :param title: Optional title for the graph
        :type title: str
        :param n_rounds: Number of rounds to simulate
        :type n_rounds: int
        :param min_players: Minimum number of players at the table
        :type min_players: int
        :param max_players: Maximum number of players at the table
        :type max_players: int
        :param n_jobs: Number of jobs to run in parallel. -1 means all processors. 1 for no parallelization.
        :type n_jobs: int
        :param print_progress: Whether to print progress
        :type print_progress: bool
        :return:
        :rtype:
        """
        if title is None:
            title = f"Pocket Pairs vs. Number of Players Win Rate"

        # Generate the dataframe
        df = self.generate(n_rounds, min_players, max_players, n_jobs, print_progress)

        title += f"\n({n_rounds} simulations per scenario)\n"

        super().visualize(df, title, n_rounds, x_ticks_suffix=" Players", n_jobs=n_jobs)

        plt.xticks(rotation=285, fontsize=15)

        plt.subplots_adjust(left=0.15, bottom=0.25)
        plt.show()
