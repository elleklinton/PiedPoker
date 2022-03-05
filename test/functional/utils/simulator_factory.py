from typing import List, Callable

from card_internals.card import Card
from player.player import Player
from round.from_table.round_simulator_from_table import RoundSimulatorFromTable
from round.native.round_simulator import RoundSimulator


class SimulatorFactory:

    SIGNATURE = Callable[[List[Card], List[Player], int], RoundSimulator]

    @staticmethod
    def round_simulator(community_cards: List[Card] = (), players: List[Player] = (), total_players: int = 5) \
            -> RoundSimulator:
        """
        Generates a round simluator object with the specified parameters
        :return: RoundSimulator object
        :rtype: RoundSimulator
        """
        return RoundSimulator(community_cards, players, total_players)

    @staticmethod
    def round_simulator_from_table(community_cards: List[Card] = (), players: List[Player] = (), total_players: int = 5):
        return RoundSimulatorFromTable(community_cards, players, total_players)
