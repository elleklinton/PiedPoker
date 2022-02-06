from card_internals.rank import Rank
from card_internals.suit import Suit


class Card:
    def __init__(self, rank: str, suit: str = None):
        if suit is None:
            assert len(rank) >= 2, 'Error: shorthand must be at least 2 characters long'
            if rank[0].isdigit():
                if rank[1].isdigit():  # Case for 10
                    self.rank = Rank(rank[:2])
                    self.suit = Suit(rank[2])
                else:  # Case for other digit 2-9
                    self.rank = Rank(rank[:1])
                    self.suit = Suit(rank[1])
            else:  # Case for royals
                self.rank = Rank(rank[:1])
                self.suit = Suit(rank[1])

            return

        self.rank = Rank(rank)
        self.suit = Suit(suit)

    def __eq__(self, other):
        # Since there will never be two cards of the same suit and rank, we only care about comparing rank
        return self.rank == other.rank

    def __gt__(self, other):
        return self.rank > other.rank

    def __lt__(self, other):
        return self.rank < other.rank

    def __str__(self):
        return f'{self.rank}{self.suit}'

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        if self.suit == Suit('s'):
            return self.rank.rank
        elif self.suit == Suit('h'):
            return 100 + self.rank.rank
        elif self.suit == Suit('d'):
            return 200 + self.rank.rank
        elif self.suit == Suit('c'):
            return 300 + self.rank.rank


