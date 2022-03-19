from typing import Union, List

from pied_poker.hand import BaseHand
from pied_poker.player import Player
from pied_poker.probability.base_poker_event import BasePokerEvent
from pied_poker.poker_round import PokerRoundResult


class PlayerHasHand(BasePokerEvent):
    def __init__(self, target_hand_type: Union[BaseHand.__class__, List[BaseHand.__class__]], player: Player = None):
        """
        Checks whether the player has the target_hand_type, which can be a type of hand, or a list of types of hands.
        E.g. both are valid values for target_hand_type:
        target_hand_type = FourOfAKind
        target_hand_type = [ThreeOfAKind, FourOfAKind]

        :type target_hand_type: Union[BaseHand.__class__, List[BaseHand.__class__]]
        :param player: Optional, if empty, defaults to first player in game
        :type player: Player
        """
        super().__init__()
        self.player = player
        self.__target_hand_type__ = target_hand_type

        if isinstance(target_hand_type, list):
            target_hands = target_hand_type
        else:
            target_hands = [target_hand_type]

        self.target_hand_ranks_set = set([h.hand_rank for h in target_hands])

    def is_event(self, round_result: PokerRoundResult) -> bool:
        if not self.player:
            self.player = round_result.player_one

        return round_result.player_during_round[self.player].hand.hand_rank in self.target_hand_ranks_set

    def __str__(self):
        return f'{self.__class__.__name__}: {self.__target_hand_type__.__name__}'

    def __repr__(self):
        return str(self)
