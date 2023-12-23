from typing import List

import pandas as pd
from matplotlib import pyplot as plt

from pied_poker.visualization.data_generator import DataGenerator
from pied_poker.card.rank import Rank
from pied_poker.card.card import Card


class StartingCardProbabilities(DataGenerator):
    def __init__(self, suited=False):
        """
        Generates data for all possible starting hands, pre-flop.
        :param suited: Whether the cards should be suited
        :type suited: bool
        """
        super().__init__(left_dimension='card_1', bottom_dimension='card_2', strength_dimension='win_rate',
                         strength_label='Win Rate')
        self.suited = suited

    @staticmethod
    def get_all_starting_cards(suited=True) -> List[List[Card]]:
        """
        Returns a list of all possible starting cards, given the suited parameter.
        :param suited: Whether the cards should be suited
        :type suited: bool
        :return: A list of all possible starting cards
        :rtype: List[List[Card]
        """
        all_starting_cards = []

        for first_rank in Rank.ALLOWED_VALUES:
            for second_rank in Rank.ALLOWED_VALUES:
                if first_rank == second_rank and suited:  # We will never have a pocket pair with the same suit
                    continue

                if suited:
                    cards = Card.of(first_rank + 's', second_rank + 's')
                else:
                    cards = Card.of(first_rank + 's', second_rank + 'c')

                all_starting_cards.append(cards)

        return all_starting_cards

    def normalize_symmetrically(self, df):
        for card_1 in df[self.left_dimension].unique():
            for card_2 in df[self.bottom_dimension].unique():
                symmetrical_rows_condition = ((df[self.left_dimension].str.contains(card_1[0])) & (
                    df[self.bottom_dimension].str.contains(card_2[0]))) | (
                                                         (df[self.left_dimension].str.contains(card_2[0])) & (
                                                     df[self.bottom_dimension].str.contains(card_1[0])))
                symmetrical_rows = df[symmetrical_rows_condition]

                if len(symmetrical_rows) > 0:
                    average = symmetrical_rows[self.strength_dimension].mean()
                    df.loc[symmetrical_rows_condition, self.strength_dimension] = average

    def generate(self, n_rounds: int = 1000, n_players=2, n_jobs=1, print_progress=True) -> pd.DataFrame:
        """
        Generates a dataframe with the probability of winning for each starting hand.
        :param print_progress: Whether to print progress
        :type print_progress: bool
        :param n_rounds: Number of rounds to simulate
        :type n_rounds: int
        :param n_players: Number of players at the table
        :type n_players: int
        :param n_jobs: Number of jobs to run in parallel. -1 means all processors.
        :type n_jobs: int
        :return:
        :rtype:
        """
        df = pd.DataFrame(columns=[self.left_dimension, self.bottom_dimension, self.strength_dimension])
        i = 0

        all_starting_cards = self.get_all_starting_cards(self.suited)

        for starting_cards in all_starting_cards:
            if i % 10 == 0 and print_progress:
                prog_pct = round(i * 100 / len(all_starting_cards), 2)
                print(f'Calculating win probabilities ({prog_pct}% done)')
            # Calculate win probability for these starting_cards
            p = self.win_probability(starting_cards, n_rounds, total_players=n_players)
            # Add row to dataframe
            df.loc[i] = [starting_cards[0], starting_cards[1], p.probability * 100]
            i += 1

        df[self.left_dimension] = df[self.left_dimension].astype(str)
        df[self.bottom_dimension] = df[self.bottom_dimension].astype(str)

        self.normalize_symmetrically(df)

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
        all_left_dimensions = [str(Card(x + 's')) for x in Rank.ALLOWED_VALUES]
        # Reverse the index so that the highest card is at the top
        all_left_dimensions = all_left_dimensions[::-1]
        df.index = pd.CategoricalIndex(df.index, categories=all_left_dimensions)
        df.sort_index(level=0, inplace=True)

        # Then, sort the columns (bottom dimension)
        left_suit = 's' if self.suited else 'c'
        all_bottom_dimensions = [str(Card(x + left_suit)) for x in Rank.ALLOWED_VALUES]

        df = df[all_bottom_dimensions]

        return df

    def visualize(self, n_rounds=1000, n_players=2, title=None, n_jobs=1, print_progress=True, x_ticks_suffix='',
                  y_ticks_suffix=''):
        """
        Visualizes the data.
        :param y_ticks_suffix: Suffix for y-axis tick labels. Default is empty string.
        :type y_ticks_suffix: str
        :param x_ticks_suffix: Suffix for x-axis tick labels. Default is empty string.
        :type x_ticks_suffix: str
        :param n_rounds: Number of rounds to simulate
        :type n_rounds: int
        :param n_players: Number of players at the table
        :type n_players: int
        :param title: Optional title of the graph
        :type title: str
        :param n_jobs: Number of jobs to run in parallel. -1 means all processors.
        :type n_jobs: int
        :param print_progress: Whether to print progress
        :type print_progress: bool
        :return:
        :rtype:
        """
        if title is None:
            suited_label = 'Suited' if self.suited else 'Unsuited'
            title = f"{suited_label} Starting Cards Win Rate"

        # Generate the dataframe
        df = self.generate(n_rounds, n_players, n_jobs, print_progress)

        title += f"\n({n_players} players, {n_rounds} simulations per scenario)\n"

        super().visualize(df, title, n_rounds, x_ticks_suffix, y_ticks_suffix, n_jobs)

        plt.show()
