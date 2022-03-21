from unittest import TestCase

from pied_poker.card.card import Card
from pied_poker.player import Player
from pied_poker.probability.events.player_wins import PlayerWins
from pied_poker.poker_round.poker_round_simulation_result import PokerRoundSimulationResult
from pied_poker.poker_round import PokerRoundResult


class TestSimulationProbability(TestCase):
    @staticmethod
    def generate_simulation_probability():
        p1 = Player('Ellek', cards=[Card('as'), Card('ad')])
        p2 = Player('Snoop', cards=[Card('10s'), Card('10d')])
        r1 = PokerRoundResult([p1, p2], [])

        p1 = Player('Ellek', cards=[Card('10d'), Card('10s')])
        p2 = Player('Snoop', cards=[Card('as'), Card('as')])
        r2 = PokerRoundResult([p1, p2], [])

        return PokerRoundSimulationResult([r1, r2])

    def test_probability_of_no_given(self):
        sp = self.generate_simulation_probability()
        r = sp.probability_of(PlayerWins(Player('Ellek')))
        self.assertEqual(r.probability, 0.5)

    def test_probability_of_with_given(self):
        sp = self.generate_simulation_probability()

        r = sp.probability_of(
            event=PlayerWins(Player('Ellek')),
            given=PlayerWins(Player('Ellek'))
        )
        self.assertEqual(r.probability, 1)

        r = sp.probability_of(
            event=PlayerWins(Player('Ellek')),
            given=PlayerWins(Player('Snoop'))
        )
        self.assertEqual(r.probability, 0)

    # def test_probability_of_and(self):
    #     sp = self.generate_simulation_probability()
    #     condition = PlayerWins().AND(PlayerHasHand(OnePair))
    #     r = sp.probability_of(
    #         event=condition
    #     )
    #     self.assertEqual(r.probability, 0.5)
    #
    #     sp = self.generate_simulation_probability()
    #     r = sp.probability_of(
    #         event=PlayerWins().AND(PlayerHasHand(TwoPair))
    #     )
    #     self.assertEqual(r.probability, 0)




