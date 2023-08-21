from typing import List, Set

from pied_poker.card.card import Card
from pied_poker.card.rank import Rank
from pied_poker.card.suit import Suit

import numpy as np


class Deck:
    ALL_CARDS = np.array([Card(rank, suit) for rank in Rank.ALLOWED_VALUES for suit in Suit.ALLOWED_VALUES])
    ALL_RANKS = [Card(rank, 's') for rank in Rank.ALLOWED_VALUES]

    def __init__(self, excluding: List[Card] = ()):
        excluding_set = set(excluding) if excluding else set()
        Deck.__check_no_duplicate_cards(excluding, excluding_set)
        self.excluded_cards = excluding_set

    @staticmethod
    def __check_no_duplicate_cards(excluding: List[Card], excluding_set: Set[Card]):
        if len(excluding_set) != len(excluding):
            raise RuntimeError(f'Error: Deck cannot have duplicate cards drawn (drawn cards: {excluding})')

    def draw(self, n=1) -> List[Card]:
        if n == 0:
            return []

        if n > len(self.ALL_CARDS) - len(self.excluded_cards):
            raise RuntimeError(f'Error: Cannot draw {n} cards from a deck with only {len(self.ALL_CARDS) - len(self.excluded_cards)} un-drawn cards.')

        drawn_cards = []
        selected_cards = np.random.choice(self.ALL_CARDS, size=n, replace=False)

        for c in selected_cards:
            # Doing it this way so we can reuse the same list for the deck of cards without having to reinitialize it
            # for every simulation which has proven to be very costly
            # Since, even in the biggest poker table with 9 players, there will only ever be 23 cards drawn from the
            # deck, we can safely assume this function will suffice for the task in the quickest way possible
            if c in self.excluded_cards:
                pass
            else:
                self.excluded_cards.add(c)
                drawn_cards.append(c)

        return drawn_cards + self.draw(n - len(drawn_cards))

    def shuffle(self, excluding: List[Card] = ()):
        """
        Shuffles the deck, with the option to exclude any cards that have already been drawn
        :param excluding:
        :type excluding:
        :return:
        :rtype:
        """
        excluding_set = set(excluding) if excluding else set()
        Deck.__check_no_duplicate_cards(excluding, excluding_set)
        self.excluded_cards = excluding_set
        return self

    def __eq__(self, other):
        return self.excluded_cards == other.excluded_cards
