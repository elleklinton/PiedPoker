from pied_poker.card.card import Card
from pied_poker.card.rank import Rank
from pied_poker.hand.flush import Flush
from pied_poker.hand import FourOfAKind, Straight
from pied_poker.hand import FullHouse
from pied_poker.probability.events.no_tie import NoTie
from pied_poker.probability.events.player_has_hand import PlayerHasHand
from pied_poker.probability.events.player_has_pocket_pair import PlayerHasPocketPair
from pied_poker.probability.events.player_wins import PlayerWins
from pied_poker.test.functional.utils.simulation_test_case import SimulationTestCase
from pied_poker.test.functional.utils.simulation_test_case_payload import SimulationTestCasePayload
from pied_poker.test.functional.utils.simulator_factory import SimulatorFactory


class TestCases(SimulationTestCase):
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

    def test_open_ended_straight_draw(self):
        """
        In this test case, we have an open-ended straight draw, and we are calculating the probability of hitting the
        straight by the river.

        We can calculate this by first calculating the probability that we do NOT hit the flush, which is:
            39/47 * 38/46

        Therefore, the probability of hitting the flush is 1 - P(not hitting flush), which is:
            1 - ((39/47) * (38/46)) = 31.5%
        """
        payload = SimulationTestCasePayload(
            simulator_factory_fn=SimulatorFactory.round_simulator,
            community_cards=[Card('10h'), Card('9d'), Card('3d')],
            player_cards=[Card('8s'), Card('7c')],
            target_event=PlayerHasHand(Straight),
            target_probability=1 - ((39/47) * (38/46)),
            delta=0.015,
        )
        self.assert_probability(payload)

    def test_gut_shot_straight_draw(self):
        """
        In this test case, we have an inside (gut-shot) straight draw, and we are calculating the probability of
        hitting the straight by the river.

        We can calculate this by first calculating the probability that we do NOT hit the straight, which is:
            43/47 * 42/46

        Therefore, the probability of hitting the flush is 1 - P(not hitting flush), which is:
            1 - ((43/47) * (42/46)) = 14.5%
        """
        payload = SimulationTestCasePayload(
            simulator_factory_fn=SimulatorFactory.round_simulator,
            community_cards=[Card('10h'), Card('jd'), Card('3d')],
            player_cards=[Card('8s'), Card('7c')],
            target_event=PlayerHasHand(Straight),
            target_probability=1 - ((43/47) * (42/46)),
            delta=0.01,
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

    def test_probability_of_pocket_aces_winning(self):
        """
        In this case, we are calculating the probability of pocket aces winning, which should be equal to 85% (if we do
        not include ties)
        """
        payload = SimulationTestCasePayload(
            simulator_factory_fn=SimulatorFactory.round_simulator,
            community_cards=[],
            player_cards=[Card('as'), Card('ad')],
            target_event=PlayerWins(),
            given_event=PlayerHasPocketPair(exact_rank=Rank('a')),
            target_probability=0.85,
            delta=0.015,
            n_players=2
        )
        self.assert_probability(payload)
