from pied_poker.hand import BaseHand
from pied_poker.player import Player
from pied_poker.probability.base_poker_event import BasePokerEvent
from pied_poker.poker_round import PokerRoundResult


class PlayerHasHandOrHigher(BasePokerEvent):
    def __init__(self, target_hand_type: BaseHand.__class__, player: Player = None):
        """
        Checks if the player has the target_hand_type, or a greater hand. E.g. if target_hand_type is FullHouse, and
        the player has FullHouse, FourOfAKind, StraightFlush, or RoyalFlush, this would return true.
        :type target_hand_type: BaseHand.__class__
        :param player: Optional, if empty, defaults to first player in game
        :type player: Player
        """
        super().__init__()
        self.player = player
        self.target_hand_type = target_hand_type

    def is_event(self, round_result: PokerRoundResult) -> bool:
        if not self.player:
            self.player = round_result.player_one
        return round_result.player_during_round[self.player].hand.hand_rank >= self.target_hand_type.hand_rank

    def __str__(self):
        return f'{self.__class__.__name__}: {self.target_hand_type}'

    def __repr__(self):
        return str(self)