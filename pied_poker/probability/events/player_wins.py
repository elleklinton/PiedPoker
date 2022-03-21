from pied_poker.player import Player
from pied_poker.probability.base_poker_event import BasePokerEvent
from pied_poker.poker_round import PokerRoundResult


class PlayerWins(BasePokerEvent):
    def __init__(self, player: Player = None, includes_tie: bool = True):
        """
        Checks whether the player wins the hand, with the option to specify if ties are considered "wins".

        :param player: Optional, if empty, defaults to first player in game
        :type player: Player
        :param includes_tie: Whether or not to count ties as a "win"
        :type includes_tie: bool
        """
        super().__init__()
        self.player = player
        self.includes_tie = includes_tie

    def is_event(self, round_result: PokerRoundResult) -> bool:
        if not self.player:
            self.player = round_result.player_one

        # This will inherently include ties
        r = self.player in round_result.winners
        if not self.includes_tie:
            r = r and len(round_result.winners) == 1
        return r

    def __str__(self):
        if self.includes_tie:
            return f'{self.__class__.__name__}: Includes Tie'
        return f'{self.__class__.__name__}: Does NOT Include Tie'

    def __repr__(self):
        return str(self)

