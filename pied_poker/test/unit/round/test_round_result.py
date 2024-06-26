from copy import deepcopy
from typing import List
from unittest import TestCase

from pied_poker.hand.killer_card import KillerCard
from pied_poker.card.card import Card
from pied_poker.hand import Flush, HighCard, OnePair
from pied_poker.hand import TwoPair
from pied_poker.hand import BaseHand
from pied_poker.hand import Straight
from pied_poker.hand import FourOfAKind
from pied_poker.hand import FullHouse
from pied_poker.hand import ThreeOfAKind
from pied_poker.hand.out import Out
from pied_poker.player import Player
from pied_poker.poker_round import PokerRoundResult


class TestRoundResult(TestCase):
    @staticmethod
    def generate_round_result(p1_cards: List[Card] = (), p2_cards: List[Card] = (), community_cards: List[Card] = ()):
        p1 = Player('Ellek', cards=p1_cards)
        p2 = Player('Snoop Dogg', cards=p2_cards)
        return PokerRoundResult([p1, p2], community_cards)

    def generate_round_p1_winning(self):
        p1_cards = [Card('as'), Card('ad')]
        p2_cards = [Card('2s'), Card('2d')]
        community_cards = [Card('ah'), Card('ac'), Card('2h'), Card('2c'), Card('10s')]
        return self.generate_round_result(p1_cards, p2_cards, community_cards)

    def test_players_ranked(self):
        result = self.generate_round_p1_winning()
        self.assertEqual(result.players_ranked, [Player('Ellek'), Player('Snoop Dogg')])

    def test_winners(self):
        result = self.generate_round_p1_winning()
        self.assertEqual(result.winners, {Player('Ellek')})

    def test_players_during_hand(self):
        result = self.generate_round_p1_winning()
        self.assertTrue(Player('Ellek') in result.player_during_round.keys())
        self.assertTrue(Player('Ellek') in result.player_during_round.values())
        self.assertTrue(Player('Snoop Dogg') in result.player_during_round.keys())
        self.assertTrue(Player('Snoop Dogg') in result.player_during_round.values())

    def test_str_winning_hand(self):
        result = self.generate_round_p1_winning()
        self.assertEqual(result.str_winning_hand(), 'FourOfAKind([A♠, A♦, A♥, A♣])')
        self.assertEqual(result.str_winning_hand(False), 'FourOfAKind')

    def test_str_winning_players_names(self):
        result = self.generate_round_p1_winning()
        self.assertEqual(result.str_winning_players_names(True, True), 'Ellek: FourOfAKind([A♠, A♦, A♥, A♣])')
        self.assertEqual(result.str_winning_players_names(False, False), 'Ellek')

    def test_winning_hand(self):
        result = self.generate_round_p1_winning()
        self.assertIsInstance(result.winning_hand, FourOfAKind)
        self.assertEqual(result.winning_hand, BaseHand([Card('as'), Card('ad'), Card('ah'), Card('ac'), Card('10s')]).as_best_hand())

    def test_empty_is_not_winner(self):
        result = self.generate_round_result([], [Card('as')], [])
        self.assertEqual(len(result.winners), 1)

    def test_outs_case_one(self):
        p1 = Player('Ellek', [Card('as'), Card('4d')])
        p2 = Player('Slim', [Card('2s'), Card('2d')])
        p3 = Player('Chris', [Card('5d'), Card('kc')])
        community_cards = [Card('10s'), Card('2h'), Card('3s'), Card('4c')]
        round_result = PokerRoundResult([p1, p2, p3], community_cards)

        p1_outs = round_result.outs(p1)

        # Ellek should have Straight outs and ThreeOfAKindKind outs.
        # The TwoPair outs are not returned here because someone on the board already has  ThreeOfAKind
        # that would beat these hands
        self.assertEqual(p1_outs, [
            Out(Straight, Card.of('5s', '5h', '5s')),
            Out(ThreeOfAKind, Card.of('4h', '4s'))
        ])

        p2_outs = round_result.outs(p2)

        # Slim should have Quad and FullHouse draws
        self.assertEqual(p2_outs, [
            Out(FourOfAKind, Card.of('2s')),
            Out(FullHouse, Card.of('10c', '10d', '10h', '4h', '4s', '3c', '3d', '3h'))
        ])

        p3_outs = round_result.outs(p3)

        self.assertEqual(p3_outs, [
            Out(Straight, Card.of('6c', '6d', '6h', '6s', 'ac', 'ad', 'ah')),
        ])

    def test_outs_case_two(self):
        p1 = Player('Ellek', [Card('as'), Card('qs')])
        p2 = Player('Slim', [])
        community_cards = Card.of('4s', '4h', '10s')
        round_result = PokerRoundResult([p1, p2], community_cards)

        p1_outs = round_result.outs(p1)

        # Ellek should have Straight outs and ThreeOfAKindKind outs.
        # The TwoPair outs are not returned here because someone on the board already has  ThreeOfAKind
        # that would beat these hands
        self.assertEqual(p1_outs, [
            Out(Flush, Card.of('2s', '3s', '5s', '6s', '7s', '8s', '9s', 'js', 'ks')),
            Out(TwoPair, Card.of('ac', 'ad', 'ah', 'qc', 'qd', 'qh'))
        ])

        p2_outs = round_result.outs(p2)

        # Slim should have Quad and FullHouse draws
        self.assertEqual(p2_outs, [
            Out(ThreeOfAKind, Card.of('4c', '4d')),
            Out(TwoPair, Card.of('10c', '10d', '10h'))
        ])

    def test_killer_cards_two_pair_with_triple_killer(self):
        p1 = Player('Ellek', [Card('8s'), Card('kc')])
        community_cards = [Card('4d'), Card('8c'), Card('4s')]
        round_result = PokerRoundResult([p1], community_cards)

        p1_killer_cards = round_result.killer_cards(p1)
        self.assertEqual(p1_killer_cards, [
            KillerCard(ThreeOfAKind, Card.of('4c', '4h'))
        ])

    def test_killer_cards_two_pair_with_with_flush_killer(self):
        p1 = Player('Ellek', [Card('10c'), Card('8d')])
        community_cards = Card.of('4s', '8s', '10s', '6s')
        round_result = PokerRoundResult([p1], community_cards)

        p1_killer_cards = round_result.killer_cards(p1)
        print(p1_killer_cards)
        self.assertEqual(p1_killer_cards, [
            KillerCard(Flush, Card.of('2s', '3s', '5s', '7s', '9s', 'js', 'qs', 'ks', 'as'))
        ])

    def test_add_and_remove_card(self):
        p1 = Player('Ellek', [Card('10s'), Card('10d')]) # Trip 10s
        p2 = Player('Slim', [Card('2s'), Card('3s')]) # Flush Draw
        community_cards = Card.of('4s', '8s', '10h', '6c')
        round_result = PokerRoundResult([p1, p2], community_cards)

        self.assertEqual(p1.hand.hand_rank, ThreeOfAKind.hand_rank)
        self.assertEqual(p2.hand.hand_rank, HighCard.hand_rank)
        self.assertIn(p1, round_result.winners)

        round_result.add_community_cards(Card('10c'))
        self.assertEqual(p1.hand.hand_rank, FourOfAKind.hand_rank)
        self.assertEqual(p2.hand.hand_rank, OnePair.hand_rank)
        self.assertIn(p1, round_result.winners)

        round_result.remove_community_cards(Card('10c'))
        self.assertEqual(p1.hand.hand_rank, ThreeOfAKind.hand_rank)
        self.assertEqual(p2.hand.hand_rank, HighCard.hand_rank)
        self.assertIn(p1, round_result.winners)

        round_result.add_community_cards(Card('6d'))
        self.assertEqual(p1.hand.hand_rank, FullHouse.hand_rank)
        self.assertEqual(p2.hand.hand_rank, OnePair.hand_rank)
        self.assertIn(p1, round_result.winners)

        round_result.remove_community_cards(Card('6d'))
        self.assertEqual(p1.hand.hand_rank, ThreeOfAKind.hand_rank)
        self.assertEqual(p2.hand.hand_rank, HighCard.hand_rank)
        self.assertIn(p1, round_result.winners)

        round_result.add_community_cards(Card('6s'))
        self.assertEqual(p1.hand.hand_rank, FullHouse.hand_rank)
        self.assertEqual(p2.hand.hand_rank, Flush.hand_rank)
        self.assertIn(p1, round_result.winners)

        round_result.remove_community_cards(Card('6s'))
        self.assertEqual(p1.hand.hand_rank, ThreeOfAKind.hand_rank)
        self.assertEqual(p2.hand.hand_rank, HighCard.hand_rank)
        self.assertIn(p1, round_result.winners)

        round_result.add_community_cards(Card('5s'))
        self.assertEqual(p1.hand.hand_rank, ThreeOfAKind.hand_rank)
        self.assertEqual(p2.hand.hand_rank, Flush.hand_rank)
        self.assertIn(p2, round_result.winners)

        round_result.remove_community_cards(Card('5s'))
        self.assertEqual(p1.hand.hand_rank, ThreeOfAKind.hand_rank)
        self.assertEqual(p2.hand.hand_rank, HighCard.hand_rank)
        self.assertIn(p1, round_result.winners)

    def test_add_and_remove_multiple_cards(self):
        p1 = Player('Ellek', [Card('10s'), Card('10d')])
        p2 = Player('Slim', [Card('2s'), Card('3s')])
        community_cards = Card.of('4s', '8s', '10h', '6c')

        round_result = PokerRoundResult([p1, p2], community_cards)
        self.assertEqual(p1.hand.hand_rank, ThreeOfAKind.hand_rank)
        self.assertEqual(p2.hand.hand_rank, HighCard.hand_rank)

        round_result.remove_community_cards(*Card.of('6c', '10h'))
        self.assertEqual(p1.hand.hand_rank, OnePair.hand_rank)
        self.assertEqual(p2.hand.hand_rank, HighCard.hand_rank)

        round_result.add_community_cards(*Card.of('10c', '10h', '6s'))
        self.assertEqual(p1.hand.hand_rank, FourOfAKind.hand_rank)
        self.assertEqual(p2.hand.hand_rank, Flush.hand_rank)

    def test_add_remove_cards_fully_reverts(self):
        p1 = Player('Ellek', [Card('As'), Card('Ad')])
        p2 = Player('Slim', [Card('Kd'), Card('8d')])
        community_cards = Card.of('4d', '7c', '7d', '7s', '2d')

        round_result_pre_flop = PokerRoundResult([p1, p2], [])
        round_result_river = PokerRoundResult([p1, p2], community_cards)

        # Add cards and check state
        self.assertEqual(round_result_pre_flop.player_one, round_result_river.player_one)
        # self.assertNotEqual(round_result_pre_flop.players_ranked, round_result_river.players_ranked)
        self.assertNotEqual(round_result_pre_flop.community_cards, round_result_river.community_cards)
        # self.assertNotEqual(round_result_pre_flop.winners, round_result_river.winners)
        self.assertEqual(round_result_pre_flop.player_cards_set, round_result_river.player_cards_set)
        self.assertNotEqual(round_result_pre_flop.community_cards_set, round_result_river.community_cards_set)

        # remove cards and check state
        round_result_river.remove_community_cards(*round_result_river.community_cards)

        self.assertEqual(round_result_pre_flop.player_one, round_result_river.player_one)
        self.assertEqual(round_result_pre_flop.players_ranked, round_result_river.players_ranked)
        self.assertEqual(round_result_pre_flop.community_cards, round_result_river.community_cards)
        self.assertEqual(round_result_pre_flop.winners, round_result_river.winners)
        self.assertEqual(round_result_pre_flop.player_cards_set, round_result_river.player_cards_set)
        self.assertEqual(round_result_pre_flop.community_cards_set, round_result_river.community_cards_set)

