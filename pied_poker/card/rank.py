from typing import Union

from pied_poker.card.comparable import Comparable


class Rank(Comparable):
    ALLOWED_VALUES = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'j', 'q', 'k', 'a']
    ALLOWED_VALUES_SET = {'2', '3', '4', '5', '6', '7', '8', '9', '10', 'j', 'q', 'k', 'a'}  # Only has '10'

    def __init__(self, value: Union[str, int]):
        if isinstance(value, int):
            super().__init__(str(value))
            self.rank = value
            return
        else:
            value = value.lower()
            if value == 't':
                self.rank = 10
            else:
                super().__init__(value)

        if value.isdigit():
            self.rank = int(value)
        elif value == 't':
            self.rank = 10
        elif value == 'j':
            self.rank = 11
        elif value == 'q':
            self.rank = 12
        elif value == 'k':
            self.rank = 13
        elif value == 'a':
            self.rank = 14

    def __eq__(self, other):
        return self.rank == other.rank

    def __gt__(self, other):
        return self.rank > other.rank

    def __ge__(self, other):
        return not self < other

    def __lt__(self, other):
        return self.rank < other.rank

    def __sub__(self, other):
        if isinstance(other, int):
            return self.rank - other
        else:
            if self.rank == 2 and other.rank == 14:  # Case for 2 - ace, should be 1
                return 1
            elif self.rank == 14 and other.rank == 2:
                return 1
            return self.rank - other.rank

    def __add__(self, other):
        if isinstance(other, int):
            return self.rank + other
        else:
            return self.rank + other.rank

    def __hash__(self):
        return self.rank

    def __str__(self):
        if self.rank <= 10:
            return super().__str__()
        elif self.rank == 11:
            return 'J'
        elif self.rank == 12:
            return 'Q'
        elif self.rank == 13:
            return 'K'
        elif self.rank == 14:
            return 'A'

    def __repr__(self):
        return super().__repr__()
