from unittest import TestCase

from main import basics_decide_to_split


class Test(TestCase):
    def test_basics_decide_to_split(self):
        self.assertEqual(basics_decide_to_split([7, 7], 6), "y")
        self.assertEqual(basics_decide_to_split([4, 4], 7), "n")
        self.assertEqual(basics_decide_to_split([5, 5], 2), "n")
        self.assertEqual(basics_decide_to_split([5, 5], 7), "n")
        self.assertEqual(basics_decide_to_split([2, 2], 7), "y")
        self.assertEqual(basics_decide_to_split([11, 11], 8), "y")
        self.assertEqual(basics_decide_to_split([10, 10], 8), "n")
        self.assertEqual(basics_decide_to_split([7, 7], 7), "y")
        self.assertEqual(basics_decide_to_split([8, 8], 8), "y")
        self.assertEqual(basics_decide_to_split([5, 5], 3), "n")

    def test_declare_winner(self):
        pass
