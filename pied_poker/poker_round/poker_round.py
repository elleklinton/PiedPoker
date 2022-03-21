from typing import List
from copy import deepcopy

from pied_poker.card.card import Card
from pied_poker.deck.deck import Deck
from pied_poker.player import Player
from pied_poker.poker_round.poker_round_result import PokerRoundResult


class PokerRound:
    def __init__(self, community_cards: List[Card] = (), players: List[Player] = (), other_drawn_cards: List[Card] = ()):
        """
        Initializes a round of poker.

        :param community_cards: The community cards
        :type community_cards: List[Card]
        :param players: The active players in the round
        :type players: List[Player]
        :param other_drawn_cards: Any other cards that have been exposed or dealt to other players that are not part of
        the community hand. E.g. If a player folded with As Ad, you would include those cards here since we know those
        cards will never be re-dealt, and cannot be used by any other player.
        :type other_drawn_cards: List[Card]
        """
        player_name_set = set()
        [player_name_set.add(p.name) for p in players]
        assert len(player_name_set) == len(players), 'Error: All players must have unique names.'

        self.community_cards: List[Card] = deepcopy(community_cards) if community_cards else []
        self.other_drawn_cards = deepcopy(other_drawn_cards) if other_drawn_cards else []
        self.players: List[Player] = deepcopy(players) if players else []
        self.deck: Deck = Deck(self.__cards_to_exclude__)

        self.__starting_deck_state__ = deepcopy(self.deck)
        self.__starting_players_state__ = deepcopy(players)
        self.__starting_community_cards_state__ = deepcopy(self.community_cards)

    def deal_cards(self):
        """
        Deals cards to all players who do not have cards
        :return:
        :rtype:
        """
        cards_needed = sum([2 - len(p.cards) for p in self.players])
        cards = self.deck.draw(cards_needed)
        for p in self.players:
            needed_cards = 2 - len(p.cards)
            p.cards.extend(cards[:needed_cards])
            cards = cards[needed_cards:]

    def simulate(self):
        """
        Deals all players cards, draws remaining community cards, and returns the RoundResult.
        RoundResult.winning_players returns a list of the players who won the hand.
        RoundResult.winning_hand returns the winning hand.

        After simulation has run, this function resets the state to the state during initialization
        :return:
        :rtype:
        """
        self.deal_cards()
        community_cards_needed = 5 - len(self.community_cards)
        community_cards_drawn = self.deck.draw(community_cards_needed)
        self.community_cards.extend(community_cards_drawn)
        r = PokerRoundResult(self.players, self.community_cards)
        self.revert_to_init_state()
        return r

    @property
    def __cards_to_exclude__(self):
        return self.community_cards + [card for player in self.players for card in player.cards] + self.other_drawn_cards

    def revert_to_init_state(self):
        """
        Resets the round to the state at time of initialization
        :return: The round object
        :rtype: PokerRound
        """
        self.deck = self.deck.shuffle(self.__cards_to_exclude__)
        self.players = [Player(p.name, p.cards, p.hand) for p in self.__starting_players_state__]
        self.community_cards = [Card(c.rank.value, c.suit.value) for c in self.__starting_community_cards_state__]
        return self

    def __repr__(self):
        return f'Players: {self.players}, Community Cards: {self.community_cards}, Other Drawn Cards: {self.other_drawn_cards}'

    def __str__(self):
        return self.__repr__()
