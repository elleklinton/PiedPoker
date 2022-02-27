from unittest import TestCase

from hands.flush import Flush
from hands.four_of_a_kind import FourOfAKind
from hands.full_house import FullHouse
from hands.high_card import HighCard
from hands.one_pair import OnePair
from hands.royal_flush import RoyalFlush
from hands.straight import Straight
from hands.straight_flush import StraightFlush
from hands.three_of_a_kind import ThreeOfAKind
from hands.two_pair import TwoPair
from hands.poker_hand import PokerHand
from test.hands.hand_test_utils import HandTestUtils


class TestPokerHand(TestCase):
    def test_as_best_hand_high_card(self):
        cards = HandTestUtils.build_shorthand('2s', '3d', '5h', '8d', '10s', 'jh', 'as')
        hand = PokerHand(cards)
        self.assertIsInstance(hand.as_best_hand(), HighCard)

    def test_as_best_hand_one_pair(self):
        cards = HandTestUtils.build_shorthand('2s', '2d', '5h', '8d', '10s', 'jh', 'as')
        hand = PokerHand(cards)
        self.assertIsInstance(hand.as_best_hand(), OnePair)

    def test_as_best_hand_two_pair(self):
        cards = HandTestUtils.build_shorthand('2s', '2d', '8h', '8d', '10s', 'jh', 'as')
        hand = PokerHand(cards)
        self.assertIsInstance(hand.as_best_hand(), TwoPair)

    def test_as_best_hand_three_of_a_kind(self):
        cards = HandTestUtils.build_shorthand('3s', '3d', '3h', '8d', '10s', 'jh', 'as')
        hand = PokerHand(cards)
        self.assertIsInstance(hand.as_best_hand(), ThreeOfAKind)

    def test_as_best_hand_straight(self):
        cards = HandTestUtils.build_shorthand('2s', '3d', '4h', '5d', '6s', 'jh', 'as')
        hand = PokerHand(cards)
        self.assertIsInstance(hand.as_best_hand(), Straight)

    def test_as_best_hand_flush(self):
        cards = HandTestUtils.build_shorthand('2d', '3d', '5d', '8d', '10s', 'jh', 'ad')
        hand = PokerHand(cards)
        self.assertIsInstance(hand.as_best_hand(), Flush)

    def test_as_best_hand_full_house(self):
        cards = HandTestUtils.build_shorthand('2s', '2d', '3h', '3d', '3s', 'jh', 'as')
        hand = PokerHand(cards)
        self.assertIsInstance(hand.as_best_hand(), FullHouse)

    def test_as_best_hand_four_of_a_kind(self):
        cards = HandTestUtils.build_shorthand('4s', '4d', '4h', '4d', '10s', 'jh', 'as')
        hand = PokerHand(cards)
        self.assertIsInstance(hand.as_best_hand(), FourOfAKind)

    def test_as_best_hand_straight_flush(self):
        cards = HandTestUtils.build_shorthand('2s', '3s', '4s', '5s', '6s', 'jh', 'as')
        hand = PokerHand(cards)
        self.assertIsInstance(hand.as_best_hand(), StraightFlush)

    def test_as_best_hand_royal_flush(self):
        cards = HandTestUtils.build_shorthand('as', 'ks', 'qs', 'js', '10s')
        hand = PokerHand(cards)
        self.assertIsInstance(hand.as_best_hand(), RoyalFlush)

    def test_hashes_unique(self):
        # Test 2 different hands (but same type) have different hashes
        cards = HandTestUtils.build_shorthand('2s', '2d', '5h', '8d', '10s', 'jh', 'as')
        hand = PokerHand(cards)

        cards_2 = HandTestUtils.build_shorthand('ad', '3d', '5h', '8d', '10s', 'jh', 'as')
        hand_2 = PokerHand(cards_2)

        assert len({hand, hand_2}) == 2, 'Error: expected set to be len 2'

    def test_hashes_unique_as_best_hand(self):
        # Test 2 different hands (but same type) have different hashes
        cards = HandTestUtils.build_shorthand('2s', '2d', '5h', '8d', '10s', 'jh', 'as')
        hand = PokerHand(cards).as_best_hand()

        cards_2 = HandTestUtils.build_shorthand('3s', '3d', '5h', '8d', '10s', 'jh', 'as')
        hand_2 = PokerHand(cards_2).as_best_hand()

        assert len({hand, hand_2}) == 2, 'Error: expected set to be len 2'

        # Test 2 different hands (DIFFERENT hand types) have different hashes
        cards = HandTestUtils.build_shorthand('as', 'ks', 'qs', 'js', '10s')
        hand = PokerHand(cards).as_best_hand()

        cards_2 = HandTestUtils.build_shorthand('3s', '3d', '5h', '8d', '10s', 'jh', 'as')
        hand_2 = PokerHand(cards_2).as_best_hand()

        assert len({hand, hand_2}) == 2, 'Error: expected set to be len 2'


