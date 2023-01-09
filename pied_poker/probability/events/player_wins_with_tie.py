from pied_poker.player import Player
from pied_poker.probability.base_poker_event import BasePokerEvent
from pied_poker.poker_round import PokerRoundResult


class PlayerWinsWithTie(BasePokerEvent):
    def __init__(self, player: Player = None):
        """
        Checks whether the player wins the hand, with the option to specify if ties are considered "wins".

        :param player: Optional, if empty, defaults to first player in game
        :type player: Player
        """
        super().__init__()
        self.player = player

    def is_event(self, round_result: PokerRoundResult) -> bool:
        if not self.player:
            self.player = round_result.player_one

        # This will inherently include ties
        r = self.player in round_result.winners
        r = r and len(round_result.winners) > 1
        return r

    def __str__(self):
        return f'{self.__class__.__name__}'

    def __repr__(self):
        return str(self)

