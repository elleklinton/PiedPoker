from pied_poker.card.comparable import Comparable


class Suit(Comparable):
    ALLOWED_VALUES = ['c', 'd', 'h', 's']  # clubs, diamonds, hearts, spades'

    def __init__(self, suit: str):
        self.__str_value__ = None
        super().__init__(suit)

    def __eq__(self, other):
        if other is None:
            return False
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
        if self.__str_value__:
            return self.__str_value__

        rv = None
        if self.value.lower() == 'c':
            rv = '♣'
        elif self.value.lower() == 'd':
            rv = '♦'
        elif self.value.lower() == 'h':
            rv = '♥'
        elif self.value.lower() == 's':
            rv = '♠'

        self.__str_value__ = rv
        return rv

    def __repr__(self):
        return self.__str__()
