from pied_poker.player import Player
from pied_poker.probability.base_poker_event import BasePokerEvent
from pied_poker.poker_round import PokerRoundResult


class PlayerLoses(BasePokerEvent):
    def __init__(self, player: Player = None):
        """
        Checks whether the player lost the hand

        :param player: Optional, if empty, defaults to first player in game
        :type player: Player
        """
        super().__init__()
        self.player = player

    def is_event(self, round_result: PokerRoundResult) -> bool:
        if not self.player:
            self.player = round_result.player_one

        return self.player not in round_result.winners

    def __str__(self):
        return f'{self.__class__.__name__}'

    def __repr__(self):
        return str(self)

