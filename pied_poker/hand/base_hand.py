from __future__ import annotations

from typing import List, Dict, Union, Set, Tuple

from pied_poker.card.card import Card
from pied_poker.card.rank import Rank
from pied_poker.card.suit import Suit
from pied_poker.hand.out import Out

# Only 6 thru A can be the highest card on a straight
STRAIGHT_POSSIBLE_HIGH_CARDS_OLD = [Rank(str(i)) for i in ['5', '6', '7', '8', '9', '10', 'j', 'q', 'k', 'a']]
STRAIGHT_POSSIBLE_HIGH_CARDS: List[Rank] = [Rank(str(i)) for i in ['a', 'k', 'q', 'j', '10', '9', '8', '7', '6', '5']]


def getAllHandsRanked() -> List[BaseHand.__class__]:
    from pied_poker.hand.flush import Flush
    from pied_poker.hand.four_of_a_kind import FourOfAKind
    from pied_poker.hand.full_house import FullHouse
    from pied_poker.hand.empty_hand import EmptyHand
    from pied_poker.hand.high_card import HighCard
    from pied_poker.hand.one_pair import OnePair
    from pied_poker.hand.royal_flush import RoyalFlush
    from pied_poker.hand.straight import Straight
    from pied_poker.hand.straight_flush import StraightFlush
    from pied_poker.hand.three_of_a_kind import ThreeOfAKind
    from pied_poker.hand.two_pair import TwoPair

    return [
        RoyalFlush,
        StraightFlush,
        FourOfAKind,
        FullHouse,
        Flush,
        Straight,
        ThreeOfAKind,
        TwoPair,
        OnePair,
        HighCard,
        EmptyHand
    ]


class StaticProperty(staticmethod):
    def __get__(self, *_):
        return self.__func__(self)


def getAllPossibleStraightRanks() -> List[set[int]]:
    """
    Returns all possible straights that can be made in poker
    :return:
    :rtype: List[List[Card]]
    """
    all_possible_straights = []
    for high_rank in STRAIGHT_POSSIBLE_HIGH_CARDS:
        if high_rank != Rank('5'):
            all_possible_straights.append({high_rank.rank, high_rank.rank - 1, high_rank.rank - 2, high_rank.rank - 3, high_rank.rank - 4})
        else:
            all_possible_straights.append({high_rank.rank, high_rank.rank - 1, high_rank.rank - 2, high_rank.rank - 3, Rank('a').rank})
    return all_possible_straights


ALL_POSSIBLE_STRAIGHTS = getAllPossibleStraightRanks()


class BaseHand:
    hand_rank: int = -1

    def __init__(self, cards: List[Card]):
        """
        For each type of hand, when initialized, it is assumed all parent hands are not present
        :param cards:
        :type cards:
        """
        self.cards_sorted: List[Card] = sorted(cards, reverse=True)  # For comparing high cards
        self.cards_set: Set[Card] = set()

        self.ranks_value_set: Set[int] = set()
        self.rank_values_set_by_suit: Dict[Suit, Set[int]] = {}

        self.ranks_single: List[Rank] = []  # All ranks of single cards, sorted
        self.ranks_pair: List[Rank] = []  # All ranks of pair cards, sorted
        self.ranks_triple: List[Rank] = []  # All ranks of triple cards, sorted
        self.ranks_quad: List[Rank] = []  # All ranks of quad cards, sorted

        self.suit_counts: Dict[Suit, int] = {}
        self.rank_counts: Dict[Rank, int] = {}

        self.flush_suit: Suit = None

        self.top_straight: List[Card] = None
        self.straight_flush: List[Card] = None

        for card in self.cards_sorted:
            self.add_card(card, True)

        self.__update_straight_and_straight_flush__()

    @StaticProperty
    def ALL_HANDS_RANKED(self) -> List[BaseHand.__class__]:
        return getAllHandsRanked()

    @property
    def is_hand(self):
        return True

    @property
    def cards_in_hand(self):
        return []

    @property
    def cards_not_in_hand(self):
        return self.cards_sorted[:5]

    def __as_hand__(self, target_class):
        self.__class__ = target_class
        return self

    def as_best_hand(self):
        for hand_class in self.ALL_HANDS_RANKED:
            # outsGetter = self.outs
            new: hand_class = self.__as_hand__(hand_class)
            if new.is_hand:  # This will always be true for EmptyHand so will always be reached
                return new

    def add_card(self, card: Card, is_init=False):
        self.cards_set.add(card)
        self.__suit_counter__(card)
        self.__rank_counter__(card)

        # insert in correct order in cards_sorted list (sorted H-L)
        if not is_init:
            insertion_index = len(self.cards_sorted)
            for i, c in enumerate(self.cards_sorted):
                if c.rank < card.rank:
                    insertion_index = i
                    break
            self.cards_sorted.insert(insertion_index, card)

        if not is_init:
            self.__update_straight_and_straight_flush__()

    def remove_card(self, card: Card):
        if card not in self.cards_set:
            raise ValueError(f'Card {card} cannot be removed because it is not in hand!')

        self.cards_sorted = [c for c in self.cards_sorted if not (c.rank == card.rank and c.suit == card.suit)]
        self.cards_set.remove(card)
        self.rank_values_set_by_suit[card.suit].remove(card.rank.rank)

        self.rank_counts[card.rank] -= 1
        self.suit_counts[card.suit] -= 1

        if self.suit_counts[card.suit] == 4:
            # If we remove a card that was part of a flush, we need to remove the flush suit
            self.flush_suit = None

        if card.rank in self.ranks_quad:
            self.ranks_quad.remove(card.rank)
            self.ranks_triple.append(card.rank)
            if len(self.ranks_triple) > 1 and self.ranks_triple[-1] > self.ranks_triple[-2]:
                self.ranks_triple = sorted(self.ranks_triple, reverse=True)
        elif card.rank in self.ranks_triple:
            self.ranks_triple.remove(card.rank)
            self.ranks_pair.append(card.rank)
            if len(self.ranks_pair) > 1 and self.ranks_pair[-1] > self.ranks_pair[-2]:
                self.ranks_pair = sorted(self.ranks_pair, reverse=True)
        elif card.rank in self.ranks_pair:
            self.ranks_pair.remove(card.rank)
            self.ranks_single.append(card.rank)
            if len(self.ranks_single) > 1 and self.ranks_single[-1] > self.ranks_single[-2]:
                self.ranks_single = sorted(self.ranks_single, reverse=True)
        elif card.rank in self.ranks_single:
            self.ranks_single.remove(card.rank)
            self.ranks_value_set.remove(card.rank.rank)

        self.__update_straight_and_straight_flush__()

    def __update_straight_and_straight_flush__(self):
        self.straight_flush = None
        self.top_straight = None

        straights = self.__get_possible_straights__()
        if len(straights) == 0:
            return

        self.top_straight = self.__get_cards_in_straight__(straights[0])
        if self.flush_suit != None:
            # Check for straight flush
            for straight in straights:
                if straight.issubset(self.rank_values_set_by_suit[self.flush_suit]):
                    self.straight_flush = self.__get_cards_in_straight__(straight, self.flush_suit)
                    return

    def __get_possible_straights__(self) -> List[Set[int]]:
        return [s for s in ALL_POSSIBLE_STRAIGHTS if s.issubset(self.ranks_value_set)]

    def __get_cards_in_straight__(self, straight: Set[int], target_suit: Union[Suit | None] = None) -> List[Card]:
        """
        Get straight cards given a set of straight ranks, optionally specifying a suit if there is a straight flush
        """
        rv: List[Card] = []
        for card in self.cards_sorted:
            if card.rank.rank in straight:
                if target_suit is not None:
                    if card.suit == target_suit:
                        rv.append(card)
                else:
                    if len(rv) == 0:
                        rv.append(card)
                    elif len(rv) > 0 and rv[-1].rank != card.rank:
                        rv.append(card)
        if Rank('a').rank in straight and Rank('2').rank in straight:
            # move ace to end
            rv.append(rv.pop(0))
        return rv

    def __suit_counter__(self, c: Card):
        self.suit_counts[c.suit] = self.suit_counts.get(c.suit, 0) + 1
        if self.suit_counts[c.suit] >= 5:
            self.flush_suit = c.suit

    def __rank_counter__(self, c: Card):
        self.rank_counts[c.rank] = self.rank_counts.get(c.rank, 0) + 1
        self.ranks_value_set.add(c.rank.rank)

        self.rank_values_set_by_suit[c.suit] = self.rank_values_set_by_suit.get(c.suit, set())
        self.rank_values_set_by_suit[c.suit].add(c.rank.rank)

        if self.rank_counts[c.rank] == 1:
            self.ranks_single.append(c.rank)
            if len(self.ranks_single) > 1 and self.ranks_single[0] < self.ranks_single[1]:
                self.ranks_single = sorted(self.ranks_single, reverse=True)

        if self.rank_counts[c.rank] == 2:
            self.ranks_single.remove(c.rank)
            self.ranks_pair.append(c.rank)
            if len(self.ranks_pair) > 1 and self.ranks_pair[-1] > self.ranks_pair[-2]:
                self.ranks_pair = sorted(self.ranks_pair, reverse=True)

        if self.rank_counts[c.rank] == 3:
            self.ranks_pair.remove(c.rank)
            self.ranks_triple.append(c.rank)
            if len(self.ranks_triple) > 1 and self.ranks_triple[-1] > self.ranks_triple[-2]:
                self.ranks_triple = sorted(self.ranks_triple, reverse=True)

        if self.rank_counts[c.rank] == 4:
            self.ranks_triple.remove(c.rank)
            self.ranks_quad.append(c.rank)
            if len(self.ranks_quad) > 1 and self.ranks_quad[-1] > self.ranks_quad[-2]:
                self.ranks_quad = sorted(self.ranks_quad, reverse=True)

    def __straight_flush_counter__(self, s: List[Card]):
        if not self.straight_flush:
            suits = set([c.suit for c in s])
            if len(suits) == 1:  # This straight is also a flush
                self.straight_flush = s

    def __eq__(self, other):
        return self.hand_rank == other.hand_rank

    def __gt__(self, other):
        return self.hand_rank > other.hand_rank

    def __lt__(self, other):
        return self.hand_rank < other.hand_rank

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f'{self.__class__.__name__}({self.cards_in_hand}, {self.cards_not_in_hand})'

    def __hash__(self):
        return str(self).__hash__()

    def __hand_outs__(self, known_cards: Set[Card]) -> List[Card]:
        """
        The outs, if any, that would make the hand. For example, if the player has a 4 flush, the remaining available
        suited cards would be returned here to complete the flush
        :return:
        :rtype: List[Card]
        """
        return []

    def outs(self, known_cards: Set[Card] = frozenset(),
             curr_winning_hand: BaseHand = None,
             should_include_equal_hand_outs=True,
             cards_in_player_hand: List[Card] = ()
             ) -> List[Out]:
        """
        All the possible one-carded outs that the player could have that are better than their current hand.
        :param known_cards: A Set of cards that are already known and cannot be used as outs
        :type known_cards: Set[Card]
        :param curr_winning_hand: The current winning hand. If not provided, will use self as the best current hand.
        :type curr_winning_hand: BaseHand
        :param should_include_equal_hand_outs: Whether to include hands of the same rank with stronger values. I.e. if
            you have a Flush, should we also return cards that would give you a higher flush? Or if someone on the board
             already has ThreeOfAKind, should we also return ThreeOfAKind that would be stronger for you?
        :type should_include_equal_hand_outs: bool
        :param cards_in_player_hand: Cards that the player exclusively holds -- we only want to return outs that are
                exclusive to the player.
        :type cards_in_player_hand:
        :return: List of outs
        :rtype: List[Out]
        """
        # This import is to avoid a circular import
        from pied_poker.hand.out import Out

        if isinstance(known_cards, frozenset):
            known_cards = set()

        if curr_winning_hand is None:
            curr_winning_hand = self

        self_original_class = self.__class__
        curr_winning_hand_class = curr_winning_hand.__class__

        rv: List[Out] = []
        known_cards_and_outs: Set[Card] = {*known_cards}

        for hand_class in self.ALL_HANDS_RANKED:
            if hand_class.hand_rank >= curr_winning_hand_class.hand_rank:
                outs = self.__as_hand__(hand_class).__hand_outs__(known_cards_and_outs)
                outs = self.__outs_with_cards_in_hand__(cards_in_player_hand, outs)

                if len(outs) > 0:
                    if hand_class.hand_rank > curr_winning_hand_class.hand_rank:
                        # In this case, we can simply return the out as it beats the current best
                        rv.append(Out(hand_class, outs))
                    elif should_include_equal_hand_outs:
                        # In this case, we need to compute the hand the player would make and compare it to the current
                        # best hand.
                        better_outs = []
                        for out in outs:
                            hand_with_out = BaseHand(self.cards_sorted + [out]).as_best_hand()
                            if hand_with_out > curr_winning_hand.__as_hand__(self_original_class):
                                better_outs.append(out)

                        if len(better_outs) > 0:
                            rv.append(Out(hand_class, better_outs))

        self.__as_hand__(self_original_class)
        curr_winning_hand.__as_hand__(curr_winning_hand_class)
        return rv

    def __outs_with_cards_in_hand__(self, cards_in_player_hand: List[Card], outs: List[Card]) -> List[Card]:
        if len(cards_in_player_hand) == 0:
            return outs

        filtered_outs = []
        for out in outs:
            hand_with_out = BaseHand(self.cards_sorted + [out]).as_best_hand()
            has_card_in_hand = sum([player_card in hand_with_out.cards_in_hand for player_card in cards_in_player_hand])
            if has_card_in_hand > 0:
                filtered_outs.append(out)

        return filtered_outs

