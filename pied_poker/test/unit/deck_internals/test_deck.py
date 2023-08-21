from random import seed
from unittest import TestCase
import numpy as np

from pied_poker.card.card import Card
from pied_poker.card.rank import Rank
from pied_poker.deck.deck import Deck


class TestDeck(TestCase):
    RANK_ALLOWED_VALUES = [v for v in Rank.ALLOWED_VALUES if v != 't']

    def test_deck_seed_works(self):
        np.random.seed(420)
        expected = [Card('kd'), Card('2s'), Card('9h'), Card('ks'), Card('jc')]
        actual = Deck().draw(5)
        self.assertListEqual(expected, actual)

    def setUp(self) -> None:
        np.random.seed(53)

    def test_subsequent_draws_do_not_redraw_same_cards(self):
        deck = Deck()
        for i in range(10000):
            drawn = set(deck.draw(7))
            drawn_again = set(deck.draw(8)) # Should be fully unique from first
            assert len(drawn_again.intersection(drawn)) == 0, \
                f'Error: redrew same cards:\nFirst draw:\n{sorted(list(drawn))}\nSecond draw:' \
                f'\n{sorted(list(drawn_again))}\nIntersection:\n{drawn.intersection(drawn_again)}'
            deck.shuffle()

    def test_does_not_redraw_excluded_cards(self):
        np.random.seed(420)
        seed(420)
        for c1 in Deck.ALL_CARDS:
            for c2 in Deck.ALL_CARDS:
                if c2 != c1:
                    forbidden = [c1, c2]
                    deck = Deck(forbidden)
                    drawn = set(deck.draw(7))
                    for d in drawn:
                        if d in set(forbidden):
                            self.fail(f'Error: Expected {d} to not be a drawn card because it was an excluded card ({forbidden})!')

    def test_each_draw_is_unique(self):
        for i in range(52):
            unique_draw_count = set(Deck().draw(i))
            self.assertEqual(len(unique_draw_count), i, f'Error: drew {i} cards but only {len(unique_draw_count)} unique cards found')

    def test_all_cards_drawn(self):
        deck = Deck()
        drawn = set()
        for i in range(52):
            drawn.add(deck.draw(1)[0])
            self.assertEqual(len(drawn), i + 1, f'Error: expected drawn to be len {i + 1} but got {len(drawn)}')

    def test_card_excluded(self):
        # Exclude all aces from deck, make sure none are ever drawn
        aces = [Card('as'), Card('ah'), Card('ac'), Card('ad')]
        deck = Deck(excluding=aces)

        drawn = set(deck.draw(48))

        self.assertEqual(len(drawn), 48, 'Error: expected to draw 48 cards')

        for a in aces:
            self.assertFalse(a in drawn, f'Error: ace found in drawn cards, should have been excluded: {a}')

    def test_draw_too_many(self):
        deck = Deck()
        deck.draw(52)

        try:
            deck.draw(1)
            self.fail('Error: expected to throw because deck has no more un-drawn cards.')
        except RuntimeError as e:
            self.assertEqual(str(e), 'Error: Cannot draw 1 cards from a deck with only 0 un-drawn cards.')

    def test_deck_cannot_have_duplicate_exclusions(self):
        excluding = Card.of('as', 'as', 'ks', 'qd')
        try:
            deck = Deck(excluding)
            self.fail('Error: expected to throw because deck has duplicate of AS card.')
        except RuntimeError as e:
            self.assertEqual(str(e), 'Error: Deck cannot have duplicate cards drawn (drawn cards: [A♠, A♠, K♠, Q♦])')
