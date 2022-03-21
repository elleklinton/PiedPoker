import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

from pied_poker.card.card import Card
from pied_poker.card.rank import Rank
from pied_poker.player import Player
from pied_poker.probability.events.player_wins import PlayerWins
from pied_poker.poker_round import PokerRoundSimulator


class PocketPairMap:
    def __init__(self):
        pass

    def visualize(self):
        df = self.calculate_probabilities()

        value_to_int = {j: i for i, j in enumerate(pd.unique(df.values.ravel()))}  # like you did
        n = len(value_to_int)
        # discrete colormap (n samples from a given cmap)
        cmap = sns.color_palette("Blues", n)
        ax = sns.heatmap(df.replace(value_to_int), cmap=cmap)
        # modify colorbar:
        colorbar = ax.collections[0].colorbar
        r = colorbar.vmax - colorbar.vmin
        colorbar.set_ticks([colorbar.vmin + r / n * (0.5 + i) for i in range(n)])
        colorbar.set_ticklabels(list(value_to_int.keys()))
        plt.show()

    def calculate_probabilities(self):
        col_names = ['pair_rank', 'num_players', 'win_pct']
        row_list = []

        for num_players in range(2, 10):  # Iterate 2 - 9 players
            for pocket_pair_rank in Rank.ALLOWED_VALUES_SET:
                player = Player('Ellek', cards=[Card(pocket_pair_rank, 's'), Card(pocket_pair_rank, 'd')])
                simulator = PokerRoundSimulator(total_players=num_players, players=[player])
                res = simulator.simulate(100, status_bar=False)

                p = res.probability_of(PlayerWins(includes_tie=True))

                row_list.append({
                    col_names[0]: pocket_pair_rank,
                    col_names[1]: num_players,
                    col_names[2]: p.probability
                })

        df = pd.DataFrame(row_list, columns=col_names)

        return df



# ppm = PocketPairMap()
# ppm.visualize()
# # df = ppm.calculate_probabilities()
#
# pass