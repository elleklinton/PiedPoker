from typing import List, Dict

from pied_poker.card.card import Card
from pied_poker.player.player import Player


class PokerRoundResult:
    def __init__(self, players: List[Player], community_cards: List[Card]):
        self.player_one = players[0]
        self.players_ranked = sorted(players, reverse=True, key=lambda p: p.poker_hand(community_cards))
        self.community_cards = community_cards
        self.winners = set([p for p in self.players_ranked if p.hand == self.players_ranked[0].hand])
        self.player_during_round: Dict[Player, Player] = {}
        for p in players:
            self.player_during_round[p] = p

    def str_winning_hand(self, include_cards: bool = True):
        hand_type = self.winning_hand.__class__.__name__
        cards_in_hand = self.winning_hand.cards_in_hand
        if include_cards:
            return f'{hand_type}({cards_in_hand})'
        return hand_type

    def str_winning_players_names(self, include_hand: bool = True, include_cards: bool = False):
        player_names = '/'.join([p.name for p in self.winners])
        if not include_hand:
            return player_names
        return f'{player_names}: {self.str_winning_hand(include_cards)}'

    @property
    def winning_hand(self):
        return self.players_ranked[0].hand

    def __str__(self):
        res = f'Community Cards: {self.community_cards}'

        for p in self.players_ranked:
            if p in self.winners:
                p_name = f"*{p.name}* (winner)"
            else:
                p_name = p.name

            sp = ' ' * 5

            s = f"\n\n{sp}{p_name}:\n{sp * 2}Cards: {p.cards}\n{sp * 2}Hand: {p.hand}"
            res += s

        return res

    def __repr__(self):
        return self.__str__()

