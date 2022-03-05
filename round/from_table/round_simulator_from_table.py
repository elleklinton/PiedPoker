from copy import deepcopy
from typing import List
from time import time

from line_profiler import LineProfiler

from card_internals.card import Card
from card_internals.rank import Rank
from player.player import Player
from probability.events.player_wins import PlayerWins
from round.from_table.player_from_table import PlayerFromTable
from round.from_table.poker_hand_table import PokerHandTable
from round.from_table.round_from_table import RoundFromTable
from round.from_table.round_result_from_table import RoundResultFromTable
from round.native.round_simulator import RoundSimulator


class RoundSimulatorFromTable(RoundSimulator):
    def __init__(self, community_cards: List[Card] = (), players: List[Player] = (), total_players: int = 5,
                 other_drawn_cards: List[Card] = ()):
        """
        Class used to simulate many poker rounds, given a current game state.
        Example Usage:
        p1 = Player('Ellek', [Card('as'), Card('ad')])
        simulator = RoundSimulator(community_cards=[], players=[p1], total_players=5)

        :param community_cards: A list of the community Card objects
        :type community_cards: List[Card]
        :param players: A list of the explicit players participating for whom hands are known.
        :type players: List[Player]
        :param total_players: The total number of players. This class will auto-generate the remaining players if
        len(players) < total_players. Default value 5.
        :type total_players: int
        """
        players = deepcopy(players) if players else []
        for i in range(total_players - len(players)):
            players.append(Player(f'player_{i}', []))

        self.poker_hand_table = PokerHandTable()
        self.round = RoundFromTable(self.poker_hand_table, community_cards, players, other_drawn_cards)
        self.players = self.round.players

    def simulate(self, n: int = 1000, n_jobs: int = 4, status_bar: bool = True):
        return super().simulate(n, 1, status_bar)


def run_pocket_pair_odds(total_players=2, n_trials=10000):
    for r in sorted(list(Rank.ALLOWED_VALUES_SET), key=lambda rr: Rank(rr)):
        p1 = Player('Ellek', [Card(f'{r}d'), Card(f'{r}s')])

        round_simulator = RoundSimulatorFromTable(players=[p1], community_cards=[], total_players=total_players)
        t = time()
        result = round_simulator.simulate(n_trials, n_jobs=1, status_bar=True)
        print(f'took {time() - t} seconds')

        prob = result.probability_of(
            event=PlayerWins(),
            given=None
        )

        print(f'Pocket {Rank(r)}s Probability of Winning with {total_players} players:\n{prob}\n')

def run(n=10000):
    p1 = Player('Dwek', [Card('6s'), Card('6h')])
    p4 = Player('Prydvor', [Card('kc'), Card('jd')])

    community_cards = []

    other_drawn_cards = []

    players = [p1, p4]

    total_players = 2

    round_simulator = RoundSimulatorFromTable(players=players, community_cards=community_cards, total_players=total_players, other_drawn_cards=other_drawn_cards)
    t = time()
    result = round_simulator.simulate(n, n_jobs=1)
    print(f'Took {time() - t} seconds')

    print(f'Probability that {p1.name} wins:')
    p = result.probability_of(
        event=PlayerWins(player=p1, includes_tie=False),
        given=None,
    )
    print(p)

    print('\n\n')

    print(f'Probability that {p4.name} wins:')
    p = result.probability_of(
        event=PlayerWins(player=p4, includes_tie=False),
        given=None,
    )
    print(p)

# t = time()
# run_pocket_pair_odds()
# print(f'total time {time() - t}')  # 44.3

# lp = LineProfiler()
# # lp.add_function(RoundFromTable.simulate)
# #
# # lp.add_function(PlayerFromTable.__init__)
# # lp.add_function(RoundResultFromTable.__init__)
# lp.add_function(PokerHandTable.make_hand)
#
#
#
#
# # lp.add_function(PokerHandTable.make_hand)
# # lp.add_function(Round.reset)
# # lp.add_function(Deck.__init__)
# # lp.add_function(Deck.shuffle)
# # lp.add_function(RoundResult.__init__)
# # lp.add_function(Player.poker_hand)
# # lp.add_function(BaseHand.__init__)
# # lp.add_function(BaseHand.__straight_counter__)
# lp_wrapper = lp(run)
# lp_wrapper()
# lp.print_stats()

# run()
