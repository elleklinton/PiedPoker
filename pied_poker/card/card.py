from pied_poker.card.rank import Rank
from pied_poker.card.suit import Suit


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
            else:  # Case for royals and T
                if rank[0].lower() == 't':
                    self.rank = Rank('10')
                else:
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
        return hash(self.__str__())

    @staticmethod
    def of(*args):
        """
        Initializes a list of Card objects from a list of input strings
        Example:
        Card.of('as', 'ad') -> [Card('as'), Card('ad')]

        :param args: The card values to initialize
        :type args: List[str]
        :return: List of Card objects
        :rtype: List[Card]
        """
        return [Card(a) for a in args]


