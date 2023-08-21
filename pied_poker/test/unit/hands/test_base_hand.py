from unittest import TestCase

from pied_poker import Player, EmptyHand
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
from pied_poker.hand import BaseHand
from pied_poker.hand.out import Out
from pied_poker.test.unit.hands.hand_test_utils import HandTestUtils


class TestBaseHand(TestCase):
    def test_as_best_hand_empty_hand(self):
        cards = []
        hand = BaseHand(cards)
        self.assertIsInstance(hand.as_best_hand(), EmptyHand)

    def test_as_best_hand_high_card(self):
        cards = HandTestUtils.build_shorthand('2s', '3d', '5h', '8d', '10s', 'jh', 'as')
        hand = BaseHand(cards)
        self.assertIsInstance(hand.as_best_hand(), HighCard)

    def test_as_best_hand_one_pair(self):
        cards = HandTestUtils.build_shorthand('2s', '2d', '5h', '8d', '10s', 'jh', 'as')
        hand = BaseHand(cards)
        self.assertIsInstance(hand.as_best_hand(), OnePair)

    def test_as_best_hand_two_pair(self):
        cards = HandTestUtils.build_shorthand('2s', '2d', '8h', '8d', '10s', 'jh', 'as')
        hand = BaseHand(cards)
        self.assertIsInstance(hand.as_best_hand(), TwoPair)

    def test_as_best_hand_three_of_a_kind(self):
        cards = HandTestUtils.build_shorthand('3s', '3d', '3h', '8d', '10s', 'jh', 'as')
        hand = BaseHand(cards)
        self.assertIsInstance(hand.as_best_hand(), ThreeOfAKind)

    def test_as_best_hand_straight(self):
        cards = HandTestUtils.build_shorthand('2s', '3d', '4h', '5d', '6s', 'jh', 'as')
        hand = BaseHand(cards)
        self.assertIsInstance(hand.as_best_hand(), Straight)

    def test_as_best_hand_flush(self):
        cards = HandTestUtils.build_shorthand('2d', '3d', '5d', '8d', '10s', 'jh', 'ad')
        hand = BaseHand(cards)
        self.assertIsInstance(hand.as_best_hand(), Flush)

    def test_as_best_hand_full_house(self):
        cards = HandTestUtils.build_shorthand('2s', '2d', '3h', '3d', '3s', 'jh', 'as')
        hand = BaseHand(cards)
        self.assertIsInstance(hand.as_best_hand(), FullHouse)

    def test_as_best_hand_four_of_a_kind(self):
        cards = HandTestUtils.build_shorthand('4s', '4d', '4h', '4d', '10s', 'jh', 'as')
        hand = BaseHand(cards)
        self.assertIsInstance(hand.as_best_hand(), FourOfAKind)

    def test_as_best_hand_straight_flush(self):
        cards = HandTestUtils.build_shorthand('2s', '3s', '4s', '5s', '6s', 'jh', 'as')
        hand = BaseHand(cards)
        self.assertIsInstance(hand.as_best_hand(), StraightFlush)

    def test_as_best_hand_royal_flush(self):
        cards = HandTestUtils.build_shorthand('as', 'ks', 'qs', 'js', '10s')
        hand = BaseHand(cards)
        self.assertIsInstance(hand.as_best_hand(), RoyalFlush)

    def test_hashes_unique(self):
        # Test 2 different hands (but same type) have different hashes
        cards = HandTestUtils.build_shorthand('2s', '2d', '5h', '8d', '10s', 'jh', 'as')
        hand = BaseHand(cards)

        cards_2 = HandTestUtils.build_shorthand('ad', '3d', '5h', '8d', '10s', 'jh', 'as')
        hand_2 = BaseHand(cards_2)

        assert len({hand, hand_2}) == 2, 'Error: expected set to be len 2'

    def test_hashes_unique_as_best_hand(self):
        # Test 2 different hands (but same type) have different hashes
        cards = HandTestUtils.build_shorthand('2s', '2d', '5h', '8d', '10s', 'jh', 'as')
        hand = BaseHand(cards).as_best_hand()

        cards_2 = HandTestUtils.build_shorthand('3s', '3d', '5h', '8d', '10s', 'jh', 'as')
        hand_2 = BaseHand(cards_2).as_best_hand()

        assert len({hand, hand_2}) == 2, 'Error: expected set to be len 2'

        # Test 2 different hands (DIFFERENT hand types) have different hashes
        cards = HandTestUtils.build_shorthand('as', 'ks', 'qs', 'js', '10s')
        hand = BaseHand(cards).as_best_hand()

        cards_2 = HandTestUtils.build_shorthand('3s', '3d', '5h', '8d', '10s', 'jh', 'as')
        hand_2 = BaseHand(cards_2).as_best_hand()

        assert len({hand, hand_2}) == 2, 'Error: expected set to be len 2'

    def test_outs_basic(self):
        cards = HandTestUtils.build_shorthand('3s', '5s', '8s', '10s')
        hand = BaseHand(cards).as_best_hand()
        self.assertEqual(hand.outs(set(), should_include_equal_hand_outs=False), [
            Out(Flush, HandTestUtils.build_shorthand('2s', '4s', '6s', '7s', '9s', 'js', 'qs', 'ks', 'as')),
            Out(OnePair, HandTestUtils.build_shorthand(
                '10c', '10d', '10h', '8c', '8d', '8h', '5c', '5d', '5h', '3c', '3d', '3h'
            ))
        ])

    def test_outs_have_no_cards_from_players(self):
        community_cards = HandTestUtils.build_shorthand('3s', '8s', '10s', 'ks')
        player_1 = Player(name='Ellek')
        player_2 = Player(name='Zoey', cards=HandTestUtils.build_shorthand('as', 'qs'))
        drawn_cards = {*community_cards, *player_1.cards, *player_2.cards}
        player_1_hand = BaseHand(cards=[*player_1.cards, *community_cards]).as_best_hand()
        player_2_hand = BaseHand(cards=[*player_2.cards, *community_cards]).as_best_hand()

        player_1_outs = player_1_hand.outs(drawn_cards, should_include_equal_hand_outs=False)
        player_2_outs = player_2_hand.outs(drawn_cards, should_include_equal_hand_outs=False)

        self.assertEqual(player_1_outs, [
            Out(Flush, HandTestUtils.build_shorthand('2s', '4s', '5s', '6s', '7s', '9s', 'js')),
            Out(OnePair, HandTestUtils.build_shorthand(
                'kc', 'kd', 'kh', '10c', '10d', '10h', '8c', '8d', '8h', '3c', '3d', '3h'
            ))
        ])

        self.assertEqual(player_2_outs, [
            Out(RoyalFlush, HandTestUtils.build_shorthand('js'))
        ])

    def test_outs_only_appear_in_highest_hand(self):
        cards = HandTestUtils.build_shorthand('3s', '5s', '8s', '10s')
        hand = BaseHand(cards).as_best_hand()
        self.assertEqual(hand.outs(should_include_equal_hand_outs=False), [
            Out(Flush, HandTestUtils.build_shorthand('2s', '4s', '6s', '7s', '9s', 'js', 'qs', 'ks', 'as')),
            Out(OnePair, HandTestUtils.build_shorthand(
                '10c', '10d', '10h', '8c', '8d', '8h', '5c', '5d', '5h', '3c', '3d', '3h'
            ))
        ])

    def test_high_card_beats_empty_hand(self):
        community_cards = []
        player_1 = Player(name='Ellek')
        player_2 = Player(name='Zoey', cards=HandTestUtils.build_shorthand('as'))
        player_1_hand = BaseHand(cards=[*player_1.cards, *community_cards]).as_best_hand()
        player_2_hand = BaseHand(cards=[*player_2.cards, *community_cards]).as_best_hand()

        self.assertTrue(player_2_hand > player_1_hand)


