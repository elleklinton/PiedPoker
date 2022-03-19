from unittest import TestCase

from pied_poker.card.card import Card
from pied_poker.hand import FourOfAKind
from pied_poker.hand import FullHouse
from pied_poker.player import Player

class TestPlayer(TestCase):
    def test_hash(self):
        # For the Player class, the hash is simply the has of the name of the player Therefore, hash is independent of
        # player state, so we would expect 2 different states of players to compute to the same hash
        player = Player('Ellek')
        player_2 = Player('Ellek', cards=[Card('as'), Card('ac')])

        self.assertEqual(len({player, player_2}), 1, 'Error: expected players to have same hash')

        # Similarly, two players with different names should have different hashes, regardless of the cards they have
        player = Player('Ellek')
        player_2 = Player('Obama')
        self.assertEqual(len({player, player_2}), 2, 'Error: expected players to have different hashes')

        player = Player('Ellek', cards=[Card('as'), Card('ac')])
        player_2 = Player('Obama', cards=[Card('as'), Card('ac')])
        self.assertEqual(len({player, player_2}), 2, 'Error: expected players to have different hashes')

        player = Player('Ellek')
        player_2 = Player('Obama', cards=[Card('as'), Card('ac')])
        self.assertEqual(len({player, player_2}), 2, 'Error: expected players to have different hashes')

    def test_poker_hand(self):
        player = Player('Ellek', cards=[Card('as'), Card('ac')])
        hand = player.poker_hand([Card('ad'), Card('ah'), Card('10d'), Card('5h'), Card('7c')])
        self.assertIsInstance(hand, FourOfAKind, 'Error: expected hand to be 4 of a kind!')

        hand = player.poker_hand([Card('ad'), Card('10s'), Card('10d'), Card('5h'), Card('7c')])
        self.assertIsInstance(hand, FullHouse, 'Error: expected hand to be a full house!')

    def test_str(self):
        player = Player('Ellek', cards=[Card('as'), Card('ac')])
        player.poker_hand([Card('ad'), Card('ah'), Card('10d'), Card('5h'), Card('7c')])
        self.assertEqual('Ellek: FourOfAKind([A♠, A♣, A♦, A♥], [10♦])', str(player))

        player.poker_hand([Card('ad'), Card('10s'), Card('10d'), Card('5h'), Card('7c')])
        self.assertEqual('Ellek: FullHouse([A♠, A♣, A♦, 10♠, 10♦], [])', str(player))




