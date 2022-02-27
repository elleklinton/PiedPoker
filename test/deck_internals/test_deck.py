from unittest import TestCase
import numpy as np

from card_internals.card import Card
from card_internals.rank import Rank
from deck_internals.deck import Deck


class TestDeck(TestCase):
    RANK_ALLOWED_VALUES = [v for v in Rank.ALLOWED_VALUES if v != 't']

    def setUp(self) -> None:
        np.random.seed(53)

    def test_subsequent_draws_do_not_redraw_same_cards(self):
        deck = Deck()
        for i in range(1000):
            drawn = set(deck.draw(8))
            drawn_again = set(deck.draw(8)) # Should be fully unique from first
            assert len(drawn_again.intersection(drawn)) == 0, \
                f'Error: redrew same cards:\nFirst draw:\n{sorted(list(drawn))}\nSecond draw:' \
                f'\n{sorted(list(drawn_again))}\nIntersection:\n{drawn.intersection(drawn_again)}'
            deck.shuffle()

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


