from unittest import TestCase

from pied_poker.card.card import Card
from pied_poker.hand import BaseHand


class HandTestUtils():
    @staticmethod
    def __card_from_shorthand__(card: str):
        assert len(card) >= 2, 'Error: shorthand must be at least 2 characters long'

        if card[0].isdigit():
            if card[1].isdigit():  # Case for 10
                return Card(card[:2], card[2])
            else:  # Case for other digit 2-9
                return Card(card[:1], card[1])
        return Card(card[0], card[1])

    @staticmethod
    def build_shorthand(*values):
        """
        Build a hand of cards from several shorthand string values.
        e.g. ('2c', '10s', 'jd', 'ah')
        """
        return [HandTestUtils.__card_from_shorthand__(c) for c in values]

    @staticmethod
    def __assert_is_hand__(test_instance: TestCase, class_type, a, b):
        test_instance.assertTrue(BaseHand(a).as_hand(class_type).is_hand, f'Test Failed:\n{BaseHand(a).as_hand(class_type)}\nwas not recognized as a hand of this class')
        test_instance.assertTrue(BaseHand(b).as_hand(class_type).is_hand, f'Test Failed:\n{BaseHand(b).as_hand(class_type)}\nwas not recognized as a hand of this class')

    @staticmethod
    def assertEquals(test_instance: TestCase, class_type, a, b):
        HandTestUtils.__assert_is_hand__(test_instance, class_type, a, b)

        test_instance.assertEqual(BaseHand(a).as_hand(class_type), BaseHand(b).as_hand(class_type), f'Test Failed:\n{BaseHand(a).as_hand(class_type)}\n!=\n{BaseHand(b).as_hand(class_type)}\n(expected eq)')
        test_instance.assertFalse(BaseHand(a).as_hand(class_type) > BaseHand(b).as_hand(class_type), f'Test Failed:\n{BaseHand(a).as_hand(class_type)}\n>\n{BaseHand(b).as_hand(class_type)}\n(expected eq)')
        test_instance.assertFalse(BaseHand(a).as_hand(class_type) < BaseHand(b).as_hand(class_type), f'Test Failed:\n{BaseHand(a).as_hand(class_type)}\n<\n{BaseHand(b).as_hand(class_type)}\n(expected eq)')

    @staticmethod
    def assertGreaterThan(test_instance: TestCase, class_type, a, b):
        HandTestUtils.__assert_is_hand__(test_instance, class_type, a, b)

        test_instance.assertNotEqual(BaseHand(a).as_hand(class_type), BaseHand(b).as_hand(class_type), f'Test Failed:\n{BaseHand(a).as_hand(class_type)}\n==\n{BaseHand(b).as_hand(class_type)}\n(expected gt)')
        test_instance.assertGreater(BaseHand(a).as_hand(class_type), BaseHand(b).as_hand(class_type), f'Test Failed:\n{BaseHand(a).as_hand(class_type)}\n!>\n{BaseHand(b).as_hand(class_type)}\n(expected gt)')
        test_instance.assertLess(BaseHand(b).as_hand(class_type), BaseHand(a).as_hand(class_type), f'Test Failed:\n{BaseHand(b).as_hand(class_type)}\n!<\n{BaseHand(a).as_hand(class_type)}\n(expected lt)')
        test_instance.assertFalse(BaseHand(a).as_hand(class_type) < BaseHand(b).as_hand(class_type), f'Test Failed:\n{BaseHand(a).as_hand(class_type)}\n<\n{BaseHand(b).as_hand(class_type)}\n(expected gt)')
        test_instance.assertFalse(BaseHand(b).as_hand(class_type) > BaseHand(a).as_hand(class_type), f'Test Failed:\n{BaseHand(a).as_hand(class_type)}\n<\n{BaseHand(b).as_hand(class_type)}\n(expected gt)')

    @staticmethod
    def assertLessThan(test_instance: TestCase, class_type, a, b):
        HandTestUtils.__assert_is_hand__(test_instance, class_type, a, b)

        test_instance.assertNotEqual(BaseHand(a).as_hand(class_type), BaseHand(b).as_hand(class_type), f'Test Failed:\n{BaseHand(a).as_hand(class_type)}\n==\n{BaseHand(b).as_hand(class_type)}\n(expected lt)')
        test_instance.assertLess(BaseHand(a).as_hand(class_type), BaseHand(b).as_hand(class_type), f'Test Failed:\n{BaseHand(a).as_hand(class_type)}\n!<\n{BaseHand(b).as_hand(class_type)}\n(expected lt)')
        test_instance.assertGreater(BaseHand(b).as_hand(class_type), BaseHand(a).as_hand(class_type), f'Test Failed:\n{BaseHand(b).as_hand(class_type)}\n!>\n{BaseHand(a).as_hand(class_type)}\n(expected gt)')
        test_instance.assertFalse(BaseHand(a).as_hand(class_type) > BaseHand(b).as_hand(class_type), f'Test Failed:\n{BaseHand(a).as_hand(class_type)}\n>\n{BaseHand(b).as_hand(class_type)}\n(expected lt)')
        test_instance.assertFalse(BaseHand(b).as_hand(class_type) < BaseHand(a).as_hand(class_type), f'Test Failed:\n{BaseHand(a).as_hand(class_type)}\n>\n{BaseHand(b).as_hand(class_type)}\n(expected lt)')

    @staticmethod
    def test_not_implemented(test_instance: TestCase, class_type):
        test_instance.assertRaises(NotImplementedError, lambda: class_type([]))



