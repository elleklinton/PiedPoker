from typing import List, Dict, Set

from pied_poker.hand.out import Out
from pied_poker.hand.killer_card import KillerCard
from pied_poker.deck.deck import Deck
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

        self.__check_unique_cards__()

    def outs(self, player: Player, should_include_equal_hand_outs=True) -> List[Out]:
        """
        All the possible one-carded outs that the player could have that are better than their current hand.

        By default, "outs" equal to the current hand rank are enabled, so for example, if the current best winning hand
        is ThreeOfAKind, but the player has a possible out with a stronger ThreeOfAKind, that out would only be returned
        if 'should_include_equal_hand_outs' is set to True.

        :param player: The player for which to calculate the outs
        :type player: Player
        :param should_include_equal_hand_outs: Whether to include hands of the same rank with stronger values. I.e. if
            you have a Flush, should we also return cards that would give you a higher flush? Or if someone on the board
             already has ThreeOfAKind, should we also return ThreeOfAKind that would be stronger for you?
        :type should_include_equal_hand_outs: bool
        :return: List of outs
        :rtype: List[Out]
        """
        cards_to_exclude: Set[Card] = set(self.community_cards)
        for other_player in self.players_ranked:
            if other_player != player:
                [cards_to_exclude.add(c) for c in other_player.cards]

        return player.hand.outs(cards_to_exclude, self.winning_hand, should_include_equal_hand_outs, player.cards)

    def killer_cards(self, player: Player) -> List[KillerCard]:
        """
        This method returns all the cards that the player would lose to, if any opponent has one of those cards.

        For example, if the board has 4-8-4 on the flop, and you have an 8, you would lose if your opponent has anu 4,
        so all the 4s would be returned here as cards that would beat that player.

        :param player: The player that we want to calculate potentially beating hands for
        :type player: Player.
        :return:
        :rtype:
        """
        # We are basically just calculating the "outs" here for a player with zero cards
        opponent = Player(player.name + '_opponent')

        hypothetical_round = PokerRoundResult([player, opponent], self.community_cards)
        opponent_outs = hypothetical_round.outs(opponent, False)

        return [KillerCard(o.out_class, o.cards) for o in opponent_outs]

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

    def __check_unique_cards__(self):
        """
        This method checks that all players have unique cards. Since we already validate this when we initialize a Deck,
        we can simply create a quiet Deck here, and rely on the Deck to throw if duplicate cards are detected.
        :return:
        :rtype:
        """
        dealt_cards = self.community_cards + [card for player in self.players_ranked for card in player.cards]
        Deck(dealt_cards)

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
