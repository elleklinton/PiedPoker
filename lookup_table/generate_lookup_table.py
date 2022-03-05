from typing import FrozenSet, Dict, List, Tuple
from tqdm import tqdm
from itertools import combinations
from math import factorial
from joblib import Parallel, delayed
import contextlib
import joblib

import scipy.stats as ss
import numpy as np

from card_internals.card import Card
from card_internals.rank import Rank
from card_internals.suit import Suit
from deck_internals.deck import Deck
from hands.base_hand import BaseHand
from hands.poker_hand import PokerHand
from lookup_table.utils.file_handler import FileHandler
from round.from_table.poker_hand_table import PokerHandTable


@contextlib.contextmanager
def tqdm_joblib(tqdm_object):
    """Context manager to patch joblib to report into tqdm progress bar given as argument"""
    class TqdmBatchCompletionCallback(joblib.parallel.BatchCompletionCallBack):
        def __call__(self, *args, **kwargs):
            tqdm_object.update(n=self.batch_size)
            return super().__call__(*args, **kwargs)

    old_batch_callback = joblib.parallel.BatchCompletionCallBack
    joblib.parallel.BatchCompletionCallBack = TqdmBatchCompletionCallback
    try:
        yield tqdm_object
    finally:
        joblib.parallel.BatchCompletionCallBack = old_batch_callback
        tqdm_object.close()




class GenerateLookupTable:
    @staticmethod
    def rank(arr: List[PokerHand]):
        arr = sorted(arr)
        curr_rank = 0
        i = 0
        ranks = []
        last_hand = None
        while i < len(arr):
            hand = arr[i]
            if not ranks:
                ranks.append(0)
            else:
                if hand == last_hand:
                    ranks.append(curr_rank)
                else:  # hand is greater
                    curr_rank += 1
                    ranks.append(curr_rank)
            last_hand = hand
            i += 1

        return arr, ranks

    @staticmethod
    def generate_lookup_dict(fp: str = 'lookup_table.pickle', min_hand_len: int = 2, max_hand_len: int = 7, n_jobs: int = -1):
        """
        Generates a multi-leveled lookup dictionary.
        First level is keyed by FrozenSet['ad']. For each FrozenSet['ad'] level-one entry, the value will be another
        dictionary with two keys:
            - poker hand type (key: 't') -> value: int
            - poker hand rank within hand (key: 'r') -> value: int

        Use LookupTableHands to map the 't' int into a poker hand class.

        Looks like this:
            {
                ...,
                frozenset( { 'as', 'ad' } )  = {
                    "t": 1
                    "r": 123456 # This will be the rank within the HAND, not globally to conserve space
                },
                ...
            }

        :param fp: The filepath to store the dictionary in
        :type fp: str
        :return: Returns the filepath where the dictionary was saved to
        :rtype: str
        """
        # lookup_table: Dict[str, Dict[str, int]] = {}
        lookup_table: Dict[int, Dict[str, int]] = {}
        all_cards_for_each_hand: Dict[BaseHand.__class__, List[PokerHand]] = {}
        grand_total = 0

        for hand_len in range(min_hand_len, max_hand_len + 1): # Generate hands of length 2 to 8
            print(f'Generating hands of {hand_len} cards')
            total_at_len = factorial(52) / (factorial(hand_len) * factorial(52 - hand_len))
            grand_total += total_at_len

            for card_combo in tqdm(combinations(Deck.ALL_CARDS, hand_len), total=total_at_len):  # Go over all combos
                # Save cards and hand rank to lookup table
                hand = PokerHand(card_combo).as_best_hand()

                key = PokerHandTable.cards_to_dict_key(hand.cards_sorted, hand.is_suit_dependent)

                hand_rank_subdict: Dict[str, int] = lookup_table.get(hand.hand_rank, {})
                hand_rank_subdict[key] = hand  # This will be overwritten with the actual rank later on
                lookup_table[hand.hand_rank] = hand_rank_subdict

                # Save hand to all_cards_for_each_hand
                # curr_list = all_cards_for_each_hand.get(hand.__class__, [])
                # curr_list.append(hand)
                # all_cards_for_each_hand[hand.__class__] = curr_list

            print('\n')

        # TODO: maybe store only by rank which will shorten possibilities for rank
        # add like suit_dependent to each hand_type

        # At this point, we have a table with all of the card_combos (lookup_table) and we have a list of all combos of
        # cards that are included in each hand (all_cards_for_each_hand)
        #
        # Now, we need to calculate the rank of each hand within that hand type, for which we will use ss.rankdata

        for hand_type, hand_value_to_hand in lookup_table.items():
            hands = list(hand_value_to_hand.values())
            print(f'Sorting hands of hand_type {hands[0].__class__}')

            hands, hand_ranks = GenerateLookupTable.rank(hands)
            all_cards_for_each_hand[hand_type] = hands
            for i in range(len(hands)):
                hand = hands[i]
                rank = hand_ranks[i]

                key = PokerHandTable.cards_to_dict_key(hand.cards_sorted, hand.is_suit_dependent)

                # key = tuple([(c.rank.rank, c.suit.value) for c in hand.cards_sorted])
                hand_rank_subdict: Dict[str, int] = lookup_table.get(hand.hand_rank, {})
                hand_rank_subdict[key] = rank
                lookup_table[hand.hand_rank] = hand_rank_subdict



        # for hand_type, hands in all_cards_for_each_hand.items():
        #     print(f'Sorting hands of hand_type {hand_type}')
        #     # hand_ranks = ss.rankdata(hands, method='ordinal')
        #     hands, hand_ranks = GenerateLookupTable.rank(hands)
        #     all_cards_for_each_hand[hand_type] = hands
        #     for i in range(len(hands)):
        #         hand = hands[i]
        #         rank = hand_ranks[i]
        #         if hand.is_suit_dependent:
        #             key = ''.join(sorted([c.dict_key for c in hand.cards_sorted], reverse=True))
        #         else:
        #             key = ''.join(sorted([f'{c.rank.value}' for c in hand.cards_sorted], reverse=True))
        #         # key = tuple([(c.rank.rank, c.suit.value) for c in hand.cards_sorted])
        #         hand_rank_subdict: Dict[str, int] = lookup_table.get(hand.hand_rank, {})
        #         hand_rank_subdict[key] = rank
        #         lookup_table[hand.hand_rank] = hand_rank_subdict


                # lookup_table[key]['r'] = rank

        FileHandler.save(lookup_table, fp)

        return fp


import time
min_cards = 7
max_cards = 7
for i in range(min_cards, max_cards + 1):
    t = time.time()
    GenerateLookupTable.generate_lookup_dict(f'lookup_table_{i}.pickle', i, i)
    print(f'Time: {time.time() - t}')

# GenerateLookupTable.generate_lookup_dict(min_hand_len=2, max_hand_len=5)


d = FileHandler.load('lookup_table_7.pickle')

# for r in Rank.ALLOWED_VALUES:
#     v = None
#     for s in Suit.ALLOWED_VALUES:
#         hand = PokerHand([Card(f'{r}{s}')])
#         if not v:
#             v = d[frozenset(hand.cards_sorted)]['r']
#         else:
#             if d[frozenset(hand.cards_sorted)]['r'] != v:
#                 for ss in Suit.ALLOWED_VALUES:
#                     h = PokerHand([Card(f'{r}{ss}')])
#                     print(f"{r}{ss}: {d[frozenset(h.cards_sorted)]['r']}")
#                 break

# Maybe store dictionary with anther rank sublevel to save space for high card which are many of ties, but do later
# only maybe saves 25% of space