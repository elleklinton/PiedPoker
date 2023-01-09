from unittest import TestCase

from pied_poker.hand.flush import Flush
from pied_poker.hand import FourOfAKind
from pied_poker.hand import FullHouse
from pied_poker.hand import HighCard
from pied_poker.hand import OnePair
from pied_poker.hand import RoyalFlush
from pied_poker.hand import Straight
from pied_poker.hand import StraightFlush
from pied_poker.hand import ThreeOfAKind
from pied_poker.hand import TwoPair
from pied_poker.hand import PokerHand
from pied_poker.test.unit.hands.hand_test_utils import HandTestUtils


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

    def test_outs(self):
        cards = HandTestUtils.build_shorthand('3s', '5s', '8s', '10s')
        hand = PokerHand(cards).as_best_hand()
        self.assertEqual(hand.outs(), {
            Flush: HandTestUtils.build_shorthand('2s', '4s', '6s', '7s', '9s', 'js', 'qs', 'ks', 'as'),
            OnePair: HandTestUtils.build_shorthand(
                '10c', '10d', '10h', '8c', '8d', '8h', '5c', '5d', '5h', '3c', '3d', '3h'
            )
        })


