from typing import List

from card_internals.card import Card
from player.player import Player
from round.from_table.poker_hand_table import PokerHandTable
from round.from_table.round_result_from_table import RoundResultFromTable
from round.native.round import Round
from round.native.round_result import RoundResult


class RoundFromTable(Round):
    def __init__(self, poker_hand_table: PokerHandTable, community_cards: List[Card] = (), players: List[Player] = (), other_drawn_cards: List[Card] = ()):
        super().__init__(community_cards, players, other_drawn_cards)
        self.poker_hand_table = poker_hand_table

    def simulate(self):
        self.deal_cards()
        community_cards_needed = 5 - len(self.community_cards)
        community_cards_drawn = self.deck.draw(community_cards_needed)
        self.community_cards.extend(community_cards_drawn)

        r = RoundResultFromTable(self.players, self.community_cards, self.poker_hand_table)
        self.revert_to_init_state()
        return r