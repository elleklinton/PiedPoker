from pied_poker.card.rank import Rank
from pied_poker.player import Player
from pied_poker.probability.base_poker_event import BasePokerEvent
from pied_poker.poker_round import PokerRoundResult


class PlayerHasPocketPair(BasePokerEvent):
    def __init__(self, player: Player = None, exact_rank: Rank = None, minimum_rank: Rank = None):
        """
        Checks whether a player has a pocket pair or not. Can be used to check for specific pocket pair, range of pocket
        pairs, or just a pocket pair in general:

        To check for a specific pocket pair, set exact_rank to the rank you are checking for. E.g. to check for a pocket
        pair of Aces, set exact_rank = Rank('a')

        To check for a pocket pair of at least a given rank, set minimum_rank to the minimum rank you are looking for.
        E.g. to check for pocket pairs greater than or equal to 5, set minimum_rank = Rank('5')

        :param player: Optional, if empty, defaults to first player in game
        :type player: Player
        :param exact_rank: A specific rank of pocket pairs that you would like this event to match
        :type exact_rank: Rank
        :param minimum_rank: The minimum rank of pocket pairs that you would like this event to match
        :type minimum_rank: Rank
        """
        super().__init__()

        if exact_rank and minimum_rank:
            raise SyntaxError('Error: you cannot specify both equal_to_rank and greater_than_rank')
        elif exact_rank:
            self.target_ranks = {exact_rank}
        else:
            if not minimum_rank:
                minimum_rank = Rank('2')

            self.target_ranks = set([Rank(r) for r in Rank.ALLOWED_VALUES_SET if Rank(r) >= minimum_rank])

        self.player = player

    def is_event(self, round_result: PokerRoundResult) -> bool:
        if not self.player:
            self.player = round_result.player_one
        actual_cards = round_result.player_during_round[self.player].cards
        return len(set([c.rank for c in actual_cards])) == 1 and actual_cards[0].rank in self.target_ranks

    def __str__(self):
        return f'{self.__class__.__name__}: {self.target_ranks}'

    def __repr__(self):
        return str(self)
