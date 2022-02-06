from card import Card
from card_internals.rank import Rank
from card_internals.suit import Suit

import numpy as np


class Deck:
    def __init__(self):
        self.available_cards = []
        self.shuffle()

    def draw(self, n=1):
        return np.random.choice(self.available_cards, size=n, replace=False)

    def shuffle(self):
        self.available_cards = np.array(
            [
                Card(rank, suit) for rank in Rank.ORDERED_ALLOWED_VALUES for suit in Suit.ORDERED_ALLOWED_VALUES
             ]
        )
