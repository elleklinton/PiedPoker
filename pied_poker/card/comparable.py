from typing import List


class Comparable:
    ALLOWED_VALUES: List[str]  # in ascending order

    def __init__(self, value: str):
        assert value.lower() in self.ALLOWED_VALUES, f'Invalid Value: {value}'
        self.value = value.lower()
        self.rank = 0

    def __str__(self):
        return f'{self.value}'

    def __repr__(self):
        return self.__str__()
