from typing import List

from card_internals.card import Card
from player.player import Player
from probability.base_poker_event import BasePokerEvent
from round.native.round_result import RoundResult


class PlayerHasCards(BasePokerEvent):
    def __init__(self, target_cards: List[Card], player: Player = None):
        """
        Checks if player was dealt ALL of the target_cards in their 2 dealt cards
        :type target_cards: List[Card]
        :param player: Optional, if empty, defaults to first player in game
        :type player: Player
        """
        super().__init__()
        self.player = player
        self.target_cards = target_cards

    def is_event(self, round_result: RoundResult) -> bool:
        if not self.player:
            self.player = round_result.player_one
        actual_cards = round_result.player_during_round[self.player].cards
        set_intersection = set(self.target_cards).intersection(actual_cards)
        return len(set_intersection) == len(set(self.target_cards))

    def __str__(self):
        return f'{self.__class__.__name__}: {self.target_cards}'

    def __repr__(self):
        return str(self)
