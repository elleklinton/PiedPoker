from unittest import TestCase

from card_internals.card import Card
from player.player import Player
from probability.events.player_wins import PlayerWins
from probability.simulation_probability import SimulationProbability
from round.native.round_result import RoundResult


class TestSimulationProbability(TestCase):
    @staticmethod
    def generate_simulation_probability():
        p1 = Player('Ellek', cards=[Card('as'), Card('ad')])
        p2 = Player('Snoop', cards=[Card('10s'), Card('10d')])
        r1 = RoundResult([p1, p2], [])

        p1 = Player('Ellek', cards=[Card('10d'), Card('10s')])
        p2 = Player('Snoop', cards=[Card('as'), Card('as')])
        r2 = RoundResult([p1, p2], [])

        return SimulationProbability([r1, r2])

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




