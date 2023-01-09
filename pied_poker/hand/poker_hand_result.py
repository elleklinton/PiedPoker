from typing import Dict, Union, List

from pied_poker.card.card import Card
from pied_poker.hand.base_hand import BaseHand


class PokerHandResult(BaseHand):
    def outs(self) -> Dict[Union[BaseHand.__class__], List[Card]]:
        """
        All of the possible one-carded outs that the player could have that are better than their current hand
        :return:
        :rtype:
        """

        rv: Dict[Union[BaseHand.__class__], List[Card]] = {}

        for hand_class in self.ALL_HANDS_RANKED:
            if hand_class.hand_rank > self.hand_rank:
                outs = self.as_hand(hand_class).__hand_outs__()
                rv[hand_class] = outs
        return rv