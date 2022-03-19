from typing import List

from pied_poker.card.card import Card
from pied_poker.probability.base_poker_event import BasePokerEvent
from pied_poker.poker_round import PokerRoundResult


class CommunityCardsInclude(BasePokerEvent):
    def __init__(self, target_cards: List[Card]):
        """
        Checks whether ALL of target_cards are included in the community cards
        :param target_cards: The target cards
        :type target_cards: List[Card]
        """
        super().__init__()
        self.target_cards = set(target_cards)

    def is_event(self, round_result: PokerRoundResult) -> bool:
        return len(self.target_cards.intersection(set(round_result.community_cards))) == len(set(self.target_cards))

    def __str__(self):
        return f'{self.__class__.__name__}: {self.target_cards}'

    def __repr__(self):
        return str(self)
