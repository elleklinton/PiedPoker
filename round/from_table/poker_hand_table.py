from typing import Dict, List

from card_internals.card import Card
from hands.poker_hand import PokerHand
from lookup_table.utils.file_handler import FileHandler
from round.from_table.poker_hand_from_table import PokerHandFromTable


# class PokerHandTable:
#     def __init__(self, min_hand_size: int = 2, max_hand_size: int = 7):
#         self.tables: Dict[int, Dict[int, Dict[str, int]]] = {}
#         # Index is:   hand_size -> hand_type -> cards_in_hand -> rank
#
#         for i in range(min_hand_size, max_hand_size + 1):  # Load lookup tables for hands ranging 2 - 7 cards
#             self.tables[i] = FileHandler.load(f'lookup_table_{i}.pickle')
#
#     @staticmethod
#     def cards_to_dict_key(cards: List[Card], is_suit_dependent: bool = False):
#         if is_suit_dependent:
#             return ''.join(sorted([c.dict_key for c in cards], reverse=True))
#         else:
#             return ''.join(sorted([f'{c.rank.value}' for c in cards], reverse=True))
#
#     def make_hand(self, cards: List[Card]):
#         key_unsuited = PokerHandTable.cards_to_dict_key(cards)
#         key_suited = PokerHandTable.cards_to_dict_key(cards, True)
#
#         for hand_rank, cards_in_hand in self.tables[len(cards)].items():
#             hand_class = PokerHand.rank_to_hand_class(hand_rank)
#
#             cards_rank = None
#
#             if key_unsuited in cards_in_hand:
#                 cards_rank = cards_in_hand[key_unsuited]
#             elif key_suited in cards_in_hand:
#                 cards_rank = cards_in_hand[key_suited]
#
#             if cards_rank is not None:
#                 return PokerHandFromTable(cards, hand_class, cards_rank)
#
#         raise ValueError(f'Error: cards ({cards}) not found in lookup table')


class PokerHandTable:
    def __init__(self, table_name: str = 'lookup_table.pickle'):
        self.lookup_table: Dict[str, Dict[str, int]] = FileHandler.load(table_name)
        # Index is:   cards_key_unsuited/suited -> { 'h': hand_rank, 'r': rank_in_hand }

    @staticmethod
    def cards_to_dict_key(cards: List[Card], is_suit_dependent: bool = False):
        if is_suit_dependent:
            return ''.join(sorted([c.dict_key for c in cards], reverse=True))
        else:
            return ''.join(sorted([f'{c.rank.value}' for c in cards], reverse=True))

    def make_hand(self, cards: List[Card]):
        key_unsuited = PokerHandTable.cards_to_dict_key(cards)
        key_suited = PokerHandTable.cards_to_dict_key(cards, True)

        hand_info = None
        if key_unsuited in self.lookup_table:
            hand_info = self.lookup_table[key_unsuited]
        elif key_suited in self.lookup_table:
            hand_info = self.lookup_table[key_suited]

        if hand_info is None:
            raise ValueError(f'Error: cards ({cards}) not found in lookup table')

        hand_rank = hand_info['h']
        hand_type = PokerHand.rank_to_hand_class(hand_rank)
        cards_rank = hand_info['r']

        return PokerHandFromTable(cards, hand_type=hand_type, cards_rank=cards_rank)


