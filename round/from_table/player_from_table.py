from typing import List

from card_internals.card import Card
from player.player import Player
from round.from_table.poker_hand_from_table import PokerHandFromTable


class PlayerFromTable(Player):
    def __init__(self, name: str, cards: List[Card] = None, hand: PokerHandFromTable = None):
        super().__init__(name, cards, hand)
        self.hand: PokerHandFromTable = hand
