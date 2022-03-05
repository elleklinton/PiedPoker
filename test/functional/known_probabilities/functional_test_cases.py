from card_internals.card import Card
from card_internals.rank import Rank
from hands.flush import Flush
from hands.four_of_a_kind import FourOfAKind
from hands.full_house import FullHouse
from player.player import Player
from probability.events.no_tie import NoTie
from probability.events.player_has_hand import PlayerHasHand
from probability.events.player_has_pocket_pair import PlayerHasPocketPair
from probability.events.player_wins import PlayerWins
from test.functional.utils.simulation_test_case import SimulationTestCase
from test.functional.utils.simulation_test_case_payload import SimulationTestCasePayload
from test.functional.utils.simulator_factory import SimulatorFactory


class TestCases(SimulationTestCase):
    # def __init__(self):
    #     super().__init__()
    #     self.simulator_factory_fn = SimulatorFactory.round_simulator_from_table

    def test_four_of_a_kind_river(self):
        """
        In this test case, we have 3 of a kind, and we are calculating the probability of drawing the 4th card, making
        four of a kind.

        Since there is 1 Ace left out of the remaining 46 cards, the probability should be 1/46.
        :return:
        :rtype:
        """
        payload = SimulationTestCasePayload(
            simulator_factory_fn=SimulatorFactory.round_simulator,
            community_cards=[Card('ah'), Card('ks'), Card('3d'), Card('7s')],
            player_cards=[Card('as'), Card('ad')],
            target_event=PlayerHasHand(FourOfAKind),
            target_probability=1/46,
            delta=0.005
        )
        self.assert_probability(payload)

    def test_full_house_river(self):
        """
        In this test case, we have 2 pair, and we are calculating the probability of drawing the another card of the
        same rank as the full pair, which would make a full house.

        Since there are 4 cards remaining that could complete the full house (ad, ac, kd, kc), the probability of
        drawing a full house on the 4/46
        :return:
        :rtype:
        """
        payload = SimulationTestCasePayload(
            simulator_factory_fn=SimulatorFactory.round_simulator,
            community_cards=[Card('ah'), Card('kh'), Card('3d'), Card('7s')],
            player_cards=[Card('as'), Card('ks')],
            target_event=PlayerHasHand(FullHouse),
            target_probability=4/46,
            delta=0.01
        )
        self.assert_probability(payload)

    def test_flush_river(self):
        """
        In this test case, we have 4 suited heart cards. We are calculating the probability that another heart will come
        on the draw.

        Out of the 13 total hearts, there are 9 remaining hearts to be drawn. Therefore, the probability of making a
        flush on the draw is 9/46
        """
        payload = SimulationTestCasePayload(
            simulator_factory_fn=SimulatorFactory.round_simulator,
            community_cards=[Card('ah'), Card('kh'), Card('3d'), Card('7s')],
            player_cards=[Card('10h'), Card('6h')],
            target_event=PlayerHasHand(Flush),
            target_probability=9/46,
            delta=0.015,
        )
        self.assert_probability(payload)

    def test_flush_draw(self):
        """
        In this test case, we have 4 suited heart cards with 2 cards remaining to be drawn. We are calculating the
        probability that at least 1 more heart will come and we make our flush.

        We can calculate this by first calculating the probability that we do NOT hit the flush, which is:
            38/47 * 37/46

        Therefore, the probability of hitting the flush is 1 - P(not hitting flush), which is:
            1 - ((38/47) * (37/46)) = 35%
        """
        payload = SimulationTestCasePayload(
            simulator_factory_fn=SimulatorFactory.round_simulator,
            community_cards=[Card('ah'), Card('kh'), Card('3d')],
            player_cards=[Card('9h'), Card('6h')],
            target_event=PlayerHasHand(Flush),
            target_probability=1 - ((38/47) * (37/46)),
            delta=0.015,
        )
        self.assert_probability(payload)

    def test_probability_of_pocket_pair(self):
        """
        In this test case, we are calculating the probability of getting any pocket pair.

        This probability is only dependent on the fact that the second card dealt is equal to the first card, which
        would be a 3/51 probability, so we expect this to have a 3/51 probability.
        """
        payload = SimulationTestCasePayload(
            simulator_factory_fn=SimulatorFactory.round_simulator,
            community_cards=[],
            player_cards=[],
            target_event=PlayerHasPocketPair(),
            target_probability=3/51,
            delta=0.008,
        )
        self.assert_probability(payload)

    def test_probability_of_specific_pocket_pair(self):
        """
        In this test case, we are calculating the probability of getting a SPECIFIC pocket pair (AA).

        This probability is:
            probability first card is Ace (4/52) * probability second card is ace given first card is Ace (3/51)
            (4/52) * (3/51)
        """
        payload = SimulationTestCasePayload(
            simulator_factory_fn=SimulatorFactory.round_simulator,
            community_cards=[],
            player_cards=[],
            target_event=PlayerHasPocketPair(exact_rank=Rank('a')),
            target_probability=(4/52) * (3/51),
            delta=0.002,
        )
        self.assert_probability(payload)

    def test_probability_of_winning(self):
        """
        In this case, we are calculating the probability of winning, which should be equal to 50% (if we do not include
        ties)
        """
        payload = SimulationTestCasePayload(
            simulator_factory_fn=SimulatorFactory.round_simulator,
            community_cards=[],
            player_cards=[],
            target_event=PlayerWins(),
            given_event=NoTie(),
            target_probability=0.5,
            delta=0.015,
            n_players=2
        )
        self.assert_probability(payload)
