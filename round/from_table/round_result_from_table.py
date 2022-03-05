from typing import List, Dict

from card_internals.card import Card
from player.player import Player
from round.from_table.player_from_table import PlayerFromTable
from round.from_table.poker_hand_from_table import PokerHandFromTable
from round.from_table.poker_hand_table import PokerHandTable
from round.native.round_result import RoundResult


class RoundResultFromTable(RoundResult):
    # noinspection PyMissingConstructor
    def __init__(self, players: List[Player], community_cards: List[Card], lookup_table: PokerHandTable):
        self.player_one = players[0]
        new_players: List[PlayerFromTable] = []

        for p in players:
            cards = p.cards + community_cards
            hand = lookup_table.make_hand(cards)
            p = PlayerFromTable(p.name, p.cards, hand)
            new_players.append(p)

        self.players_ranked = sorted(new_players,
                                     reverse=True,
                                     key=lambda p: p.hand)

        self.community_cards = community_cards
        self.winners = set([p for p in self.players_ranked if p.hand == self.players_ranked[0].hand])
        self.player_during_round: Dict[Player, Player] = {}
        for p in new_players:
            self.player_during_round[p] = p

    def str_winning_hand(self, include_cards: bool = True):
        hand_type = self.winning_hand.hand_type.__class__.__name__
        cards_in_hand = self.winning_hand.cards_sorted
        if include_cards:
            return f'{hand_type}({cards_in_hand})'
        return hand_type
