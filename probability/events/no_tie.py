from player.player import Player
from probability.base_poker_event import BasePokerEvent
from round.native.round_result import RoundResult


class NoTie(BasePokerEvent):
    def __init__(self):
        """
        Checks whether the player wins the hand, with the option to specify if ties are considered "wins".

        :param player: Optional, if empty, defaults to first player in game
        :type player: Player
        :param includes_tie: Whether or not to count ties as a "win"
        :type includes_tie: bool
        """
        super().__init__()

    def is_event(self, round_result: RoundResult) -> bool:
        return len(round_result.winners) == 1

    def __str__(self):
        return f'{self.__class__.__name__}'

    def __repr__(self):
        return str(self)

