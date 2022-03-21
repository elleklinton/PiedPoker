from typing import List

from pied_poker.card import Card, Rank
from pied_poker.player import Player
from pied_poker.poker_round import PokerRoundSimulator
from pied_poker.probability import PlayerWins
from pied_poker.visualization.heatmap.heatmap_dimension import HeatmapDimension
from pied_poker.visualization.heatmap.heatmap_dimension_value import HeatmapDimensionValue
from pied_poker.visualization.heatmap.heatmap_generator import HeatmapGenerator


class PocketPairVsNumPlayersHeatmap(HeatmapGenerator):
    def __init__(self, n_rounds: int = 1000, n_jobs=-1):
        card_pairs = [HeatmapDimensionValue(Card.of(f'{r}s', f'{r}c')) for r in reversed(Rank.ALLOWED_VALUES)]
        cards_dimension = HeatmapDimension(card_pairs, 'Starting Cards')

        num_players = [HeatmapDimensionValue(p, f'{p} Players') for p in list(range(2, 10))]
        num_players_dimensions = HeatmapDimension(num_players, 'Number of Players')

        super().__init__(left_dimension=cards_dimension, bottom_dimension=num_players_dimensions)
        self.n_rounds = n_rounds
        self.n_jobs = n_jobs

    def probability_of(self, left_value: HeatmapDimensionValue[List[Card]], bottom_value: HeatmapDimensionValue[int]) \
            -> float:
        p1 = Player('Ellek', cards=left_value.value)
        round_simulator = PokerRoundSimulator(players=[p1], total_players=bottom_value.value)
        result = round_simulator.simulate(self.n_rounds, n_jobs=self.n_jobs, status_bar=False)
        return result.probability_of(PlayerWins()).probability
