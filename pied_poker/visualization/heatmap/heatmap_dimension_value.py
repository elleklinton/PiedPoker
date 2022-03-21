from typing import TypeVar, Generic

T = TypeVar('T')


class HeatmapDimensionValue(Generic[T]):
    def __init__(self, value: T, label: str = None):
        self.value = value
        if label is None:
            label = str(value)
        self.label = label

    def __str__(self):
        return f'{self.value}'

    def __repr__(self):
        return str(self)