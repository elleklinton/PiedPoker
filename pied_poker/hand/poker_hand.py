# from typing import List, Dict, Union, Set
#
# from pied_poker.card.card import Card
# from pied_poker.hand.flush import Flush
# from pied_poker.hand.four_of_a_kind import FourOfAKind
# from pied_poker.hand.full_house import FullHouse
# from pied_poker.hand.high_card import HighCard
# from pied_poker.hand.one_pair import OnePair
# from pied_poker.hand.royal_flush import RoyalFlush
# from pied_poker.hand.straight import Straight
# from pied_poker.hand.straight_flush import StraightFlush
# from pied_poker.hand.three_of_a_kind import ThreeOfAKind
# from pied_poker.hand.two_pair import TwoPair
# from pied_poker.hand.base_hand import BaseHand
#
# ALL_HANDS_RANKED = [
#         RoyalFlush,
#         StraightFlush,
#         FourOfAKind,
#         FullHouse,
#         Flush,
#         Straight,
#         ThreeOfAKind,
#         TwoPair,
#         OnePair,
#         HighCard
#     ]
#
#
# # class PokerHand(BaseHand):
# class PokerHand:
#     ALL_HANDS_RANKED = ALL_HANDS_RANKED
#
#     def __init__(self, cards: List[Card]):
#         """A class used to represent a hand of cards in poker.
#
#         Used to compare different hands to find the greater hand.
#         Example:
#         cards = [Card('ah'), Card('ad'), Card('as'), Card('kh'), Card('kd')]
#         hand = PokerHand(cards)
#         hand.as_best_hand() # Converts the hand to a FullHouse hand type since that's the best hand
#         hand.is_hand # returns True because the hand is a full house
#
#         :param cards: Cards in the hand
#         :type cards: List[Card]
#         """
#         self.cards = cards
#
#     def as_hand(self, target_class):
#         """
#         Converts this generic hand to a specific class of hand
#         :param target_class:
#         :type target_class:
#         :return:
#         :rtype:
#         """
#         return super().as_hand(target_class)
#
#     def as_best_hand(self):
#         for hand_class in self.ALL_HANDS_RANKED:
#             # outsGetter = self.outs
#             new: hand_class = self.as_hand(hand_class)
#             new.outsGetter = lambda: PokerHand.outs(self)
#             if new.is_hand:  # This will always be true for HighCard, so this will always be reached
#                 return new
#
#     def outs(self) -> Dict[Union[BaseHand.__class__], List[Card]]:
#         """
#         All of the possible one-carded outs that the player could have that are better than their current hand
#         :return:
#         :rtype:
#         """
#         original_class = self.__class__
#         rv: Dict[Union[BaseHand.__class__], List[Card]] = {}
#         out_cards: Set[Card] = set()
#
#         for hand_class in PokerHand.ALL_HANDS_RANKED:
#             if hand_class.hand_rank > original_class.hand_rank:
#                 outs = self.as_hand(hand_class).__hand_outs__()
#                 outs_available = [o for o in outs if (o not in known_cards and o not in out_cards)]
#                 if len(outs_available) > 0:
#                     rv[hand_class] = outs_available
#                     out_cards = out_cards.union(outs_available)
#
#         self.as_hand(original_class)
#         return rv
#
#     def __hash__(self):
#         return super(PokerHand, self).__hash__()
from pied_poker.hand.base_hand import BaseHand


class PokerHand(BaseHand):
    pass