from __future__ import annotations

from round.native.round_result import RoundResult


class BasePokerEvent:
    def __init__(self):
        self.filter_fn = self.is_event

    def is_event(self, round_result: RoundResult) -> bool:
        raise NotImplementedError('Error: PokerEvent.is_event is undefined')

    def __str__(self):
        return f'{self.__class__.__name__}'

    def __repr__(self):
        return str(self)

    # def AND(self, other: Union[BasePokerEvent, Callable[[RoundResult], bool]]) -> BasePokerEvent:
    #     if isinstance(other, BasePokerEvent):
    #         other = other.filter_fn
    #     self.filter_fn = lambda r: self.filter_fn(r) and other(r)
    #     return self
    #
    # def OR(self, other: Union[BasePokerEvent, Callable[[RoundResult], bool]]) -> BasePokerEvent:
    #     if isinstance(other, BasePokerEvent):
    #         other = other.filter_fn
    #     self.filter_fn = lambda r: self.filter_fn(r) or other(r)
    #     return self
