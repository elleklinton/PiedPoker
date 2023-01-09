from pied_poker.card.comparable import Comparable


class Suit(Comparable):
    ALLOWED_VALUES = ['c', 'd', 'h', 's']  # clubs, diamonds, hearts, spades'

    def __init__(self, suit: str):
        super().__init__(suit)

    def __eq__(self, other):
        return self.value == other.value

    def __hash__(self):
        if self.value == 'c':
            return 0
        if self.value == 'd':
            return 1
        if self.value == 'h':
            return 2
        return 3

    def __str__(self):
        if self.value.lower() == 'c':
            return '♣'
        elif self.value.lower() == 'd':
            return '♦'
        elif self.value.lower() == 'h':
            return '♥'
        elif self.value.lower() == 's':
            return '♠'

    def __repr__(self):
        return self.__str__()
