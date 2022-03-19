from pied_poker.player import Player
from pied_poker.probability.base_poker_event import BasePokerEvent
from pied_poker.poker_round import PokerRoundResult


class PlayerHasSuitedCards(BasePokerEvent):
    def __init__(self, player: Player = None, only_suited_connectors: bool = False):
        """
        Checks whether the player has suited cards, with the option to only check for suited connector cards, which
        are defined as sequential cards of the same suit
        :param player: Optional, if empty, defaults to first player in game
        :type player: Player
        :param only_suited_connectors: Whether this should only check for suited connector cards
        :type only_suited_connectors: bool
        """
        super().__init__()
        self.player = player
        self.only_suited_connectors = only_suited_connectors

    def is_event(self, round_result: PokerRoundResult) -> bool:
        if not self.player:
            self.player = round_result.player_one
        actual_cards = round_result.player_during_round[self.player].cards
        card_suits = set([c.suit for c in actual_cards])
        if self.only_suited_connectors:
            return len(card_suits) == 1 and abs(actual_cards[0].rank - actual_cards[1].rank) == 1
        return len(card_suits) == 1

    def __str__(self):
        if self.only_suited_connectors:
            return f'{self.__class__.__name__}: Only Suited Connectors'
        return self.__class__.__name__

    def __repr__(self):
        return str(self)
