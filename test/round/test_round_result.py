from typing import List
from unittest import TestCase

from card_internals.card import Card
from hands.four_of_a_kind import FourOfAKind
from hands.poker_hand import PokerHand
from player.player import Player
from round.round_result import RoundResult


class TestRoundResult(TestCase):
    @staticmethod
    def generate_round_result(p1_cards: List[Card] = (), p2_cards: List[Card] = (), community_cards: List[Card] = ()):
        p1 = Player('Ellek', cards=p1_cards)
        p2 = Player('Snoop Dogg', cards=p2_cards)
        return RoundResult([p1, p2], community_cards)

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
        self.assertEqual(result.winning_hand, PokerHand([Card('as'), Card('ad'), Card('ah'), Card('ac'), Card('10s')]).as_best_hand())
