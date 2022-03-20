from typing import List

from pied_poker.card import Card, Rank
from pied_poker.player import Player
from pied_poker.poker_round import PokerRoundSimulator
from pied_poker.probability import PlayerWins
from pied_poker.visualization.heatmap.heatmap_dimension import HeatmapDimension
from pied_poker.visualization.heatmap.heatmap_dimension_value import HeatmapDimensionValue
from pied_poker.visualization.heatmap.heatmap_generator import HeatmapGenerator


class AllSuitedStartingHands(HeatmapGenerator):
    def __init__(self, n_rounds: int = 1000, n_jobs=-1):
        cards = [HeatmapDimensionValue(Card(f'{r}s')) for r in reversed(Rank.ALLOWED_VALUES)]
        cards_dimension = HeatmapDimension(cards, 'Card')
        other_cards_dimension = HeatmapDimension(cards, 'Card')

        super().__init__(left_dimension=cards_dimension, bottom_dimension=other_cards_dimension)
        self.n_rounds = n_rounds
        self.n_jobs = n_jobs

    def visualize(self, title: str = None):
        super().visualize('Starting Suited Cards')

    def probability_of(self, left_value: HeatmapDimensionValue[Card], bottom_value: HeatmapDimensionValue[Card]) \
            -> float:
        if left_value.value == bottom_value.value:
            return None
        elif left_value.value < bottom_value.value:
            p1 = Player('Ellek', cards=[left_value.value, bottom_value.value])
            round_simulator = PokerRoundSimulator(players=[p1], total_players=2)
            result = round_simulator.simulate(self.n_rounds, n_jobs=self.n_jobs, status_bar=False)
            return result.probability_of(PlayerWins()).probability
        else:
            return None
