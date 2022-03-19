from typing import List

from pied_poker.card.suit import Suit
from pied_poker.player import Player
from pied_poker.probability.base_poker_event import BasePokerEvent
from pied_poker.poker_round import PokerRoundResult


class PlayerHasCardSuits(BasePokerEvent):
    def __init__(self, target_suits: List[Suit], player: Player = None):
        """
        Checks whether the player has ALL of the target Suits in their 2 dealt cards
        :type target_suits: List[Rank]
        :param player: Optional, if empty, defaults to first player in game
        :type player: Player
        """
        super().__init__()
        self.player = player
        self.target_suits = target_suits

    def is_event(self, round_result: PokerRoundResult) -> bool:
        if not self.player:
            self.player = round_result.player_one
        actual_cards = round_result.player_during_round[self.player].cards
        set_intersection = set(self.target_suits).intersection(set([c.suit for c in actual_cards]))
        return len(set_intersection) == len(set(self.target_suits))

    def __str__(self):
        return f'{self.__class__.__name__}: {self.target_suits}'

    def __repr__(self):
        return str(self)
