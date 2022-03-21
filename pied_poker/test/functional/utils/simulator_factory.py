from typing import List, Callable

from pied_poker.card.card import Card
from pied_poker.player import Player
from pied_poker.poker_round import PokerRoundSimulator


class SimulatorFactory:

    SIGNATURE = Callable[[List[Card], List[Player], int], PokerRoundSimulator]

    @staticmethod
    def round_simulator(community_cards: List[Card] = (), players: List[Player] = (), total_players: int = 5) \
            -> PokerRoundSimulator:
        """
        Generates a round simluator object with the specified parameters
        :return: RoundSimulator object
        :rtype: PokerRoundSimulator
        """
        return PokerRoundSimulator(community_cards, players, total_players)
