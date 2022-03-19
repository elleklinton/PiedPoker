"""
Probability of winning given pocket pair (5 players):
2: 16.73% == 1:5.98 odds == (3347/20000)
3: 17.77% == 1:5.63 odds == (3553/20000)
4: 18.75% == 1:5.33 odds == (3751/20000)
5: 19.65% == 1:5.09 odds == (3929/20000)
6: 21.11% == 1:4.74 odds == (4222/20000)
7: 23.31% == 1:4.29 odds == (4662/20000)
8: 24.7% == 1:4.05 odds == (4941/20000)
9: 26.9% == 1:3.72 odds == (5380/20000)
T: 29.68% == 1:3.37 odds == (5936/20000)
J: 32.68% == 1:3.06 odds == (6536/20000)
Q: 36.21% == 1:2.76 odds == (7242/20000)
K: 41.23% == 1:2.43 odds == (8246/20000)
A: 45.12% == 1:2.22 odds == (9023/20000)
"""
from time import time

from pied_poker.card import Card

from pied_poker.card import Rank
from pied_poker.player import Player
from pied_poker.probability.events.player_wins import PlayerWins
from pied_poker.poker_round import PokerRoundSimulator as RoundSimulator

"""
Probability of winning given pocket pair (2 players):
2: 45.38% == 1:2.2 odds == (9075/20000)
3: 48.55% == 1:2.06 odds == (9710/20000)
4: 51.28% == 1:1.95 odds == (10255/20000)
5: 54.88% == 1:1.82 odds == (10976/20000)
6: 58.16% == 1:1.72 odds == (11632/20000)
7: 60.63% == 1:1.65 odds == (12126/20000)
8: 63.84% == 1:1.57 odds == (12768/20000)
9: 66.96% == 1:1.49 odds == (13392/20000)
T: 69.86% == 1:1.43 odds == (13973/20000)
J: 72.38% == 1:1.38 odds == (14475/20000)
Q: 74.64% == 1:1.34 odds == (14928/20000)
K: 77.35% == 1:1.29 odds == (15470/20000)
A: 80.38% == 1:1.24 odds == (16076/20000)
"""
"""
Pocket 2s Probability of Winning with 2 players:
51.62% == 1:1.94 odds == (10323/20000)

Pocket 3s Probability of Winning with 2 players:
55.34% == 1:1.81 odds == (11069/20000)

Pocket 4s Probability of Winning with 2 players:
57.98% == 1:1.72 odds == (11595/20000)

Pocket 5s Probability of Winning with 2 players:
61.51% == 1:1.63 odds == (12302/20000)

Pocket 6s Probability of Winning with 2 players:
64.37% == 1:1.55 odds == (12874/20000)

Pocket 7s Probability of Winning with 2 players:
66.55% == 1:1.5 odds == (13311/20000)

Pocket 8s Probability of Winning with 2 players:
69.43% == 1:1.44 odds == (13886/20000)

Pocket 9s Probability of Winning with 2 players:
72.72% == 1:1.38 odds == (14545/20000)

Pocket 10s Probability of Winning with 2 players:
74.79% == 1:1.34 odds == (14958/20000)

Pocket Js Probability of Winning with 2 players:
77.31% == 1:1.29 odds == (15461/20000)

Pocket Qs Probability of Winning with 2 players:
79.95% == 1:1.25 odds == (15990/20000)

Pocket Ks Probability of Winning with 2 players:
82.58% == 1:1.21 odds == (16516/20000)

Pocket As Probability of Winning with 2 players:
85.65% == 1:1.17 odds == (17129/20000)
"""


def run_pocket_pair_odds(total_players=2, n_trials=1000):
    for r in sorted(list(Rank.ALLOWED_VALUES_SET), key=lambda rr: Rank(rr)):
        p1 = Player('Ellek', [Card(f'{r}d'), Card(f'{r}s')])

        round_simulator = RoundSimulator(players=[p1], community_cards=[], total_players=total_players)
        t = time()
        result = round_simulator.simulate(n_trials, n_jobs=-1, status_bar=False)

        prob = result.probability_of(
            event=PlayerWins(),
            given=None
        )

        print(f'Pocket {Rank(r)}s Probability of Winning with {total_players} players:\n{prob}\n')


def run(n=1000):
    p1 = Player('Dwek', [Card('6s'), Card('6h')])
    # p2 = Player('Woo', [Card('9h'), Card('6c')])
    # p3 = Player('Dobric', [Card('qd'), Card('10d')])
    p4 = Player('Prydvor', [Card('kc'), Card('jd')])
    # p5 = Player('Mitchell', [Card('ks'), Card('9d')])
    # p6 = Player('Gerber', [Card('ah'), Card('7s')])
    # p7 = Player('Beebe', [Card('qs'), Card('5c')])

    community_cards = []
    community_cards = [Card('10h'), Card('jc'), Card('4c'), Card('5h')]

    other_drawn_cards = [Card('qd'), Card('10d')] + [Card('kc'), Card('jd')] + [Card('ks'), Card('9d')] + [Card('ah'), Card('7s')] + [Card('qs'), Card('5c')]
    # other_drawn_cards = []

    players = [p1, p4]

    total_players = 2

    round_simulator = RoundSimulator(players=players, community_cards=community_cards, total_players=total_players, other_drawn_cards=other_drawn_cards)
    t = time()
    result = round_simulator.simulate(n, n_jobs=-1)
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

    # p = result.probability_of(
    #     event=PlayerWins(),
    #     given=None
    # )
    # print(p)
    #
    # p = result.probability_of(
    #     event=PlayerWins(includes_tie=False),
    #     given=None
    # )
    # print(p)

    # p = result.probability_of(
    #     event=PlayerHasHand(RoyalFlush),
    #     given=None
    # )
    # print(p)


# lp = LineProfiler()
# lp.add_function(Round.simulate)
# lp.add_function(Round.reset)
# lp.add_function(Deck.__init__)
# lp.add_function(Deck.shuffle)
# lp.add_function(RoundResult.__init__)
# lp.add_function(Player.poker_hand)
# lp.add_function(BaseHand.__init__)
# lp.add_function(BaseHand.__straight_counter__)
# lp_wrapper = lp(run)
# lp_wrapper()
# lp.print_stats()

run_pocket_pair_odds(3)
# run(20000)
