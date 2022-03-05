from typing import Dict

from lookup_table.utils.file_handler import FileHandler
from round.from_table.poker_hand_table import PokerHandTable


class MergeLookupTables:
    def __init__(self, min_hand_size: int = 1, max_hand_size: int = 7):
        self.tables: Dict[int, Dict[int, Dict[str, int]]] = {}
        # Index is:   hand_size -> hand_type -> cards_in_hand -> rank

        for i in range(min_hand_size, max_hand_size + 1):  # Load lookup tables for hands ranging 2 - 7 cards
            self.tables[i] = FileHandler.load(f'lookup_table_{i}.pickle')

    def merge(self, export_name: str = 'lookup_table.pickle'):
        new_d = {}
        for card_count in self.tables.keys():
            print(f'Getting hands of {card_count} size')
            for hand_rank, cards_in_hand_dict in self.tables[card_count].items():
                for cards_key, rank_in_hand in cards_in_hand_dict.items():
                    new_d[cards_key] = {
                        'h': hand_rank,
                        'r': rank_in_hand
                    }
        FileHandler.save(new_d, export_name)
        return new_d




d = MergeLookupTables().merge()
