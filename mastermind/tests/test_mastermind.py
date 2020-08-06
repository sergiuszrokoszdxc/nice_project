import unittest

from mastermind.mastermind import Mastermind, MaxTriesExceeded, SequenceNonValid


class TestMastermind(unittest.TestCase):

    def test_win(self):
        """in progress"""
        mm = Mastermind()
        res = mm.guess(mm._sequence)
        self.assertIsInstance(res, tuple)
        self.assertEqual(len(res), 2)
        self.assertEqual(res[1], 0)
        self.assertEqual(res[0], len(mm._sequence))

    def test_guess(self):
        """in progress"""
        mm = Mastermind()
        res = mm.guess(tuple(reversed(mm._sequence)))
        self.assertIsInstance(res, tuple)
        self.assertEqual(len(res), 2)
        self.assertEqual(res[0], 0)
        self.assertEqual(res[1], len(mm._sequence))

    def test_validate(self):
        """in progress"""
        mm = Mastermind(n_colours=4, n_pos=3)
        mm._validate((1, 2, 3))
        with self.assertRaises(SequenceNonValid):
            mm._validate((1, 2, 5))
        with self.assertRaises(SequenceNonValid):
            mm._validate((1, 2, -1))
        with self.assertRaises(SequenceNonValid):
            mm._validate((1, 2, 5, 3))
        with self.assertRaises(SequenceNonValid):
            mm._validate((1, 2))

    def test_exceed_max_tries(self):
        """in progress"""
        mm = Mastermind(max_tries=3)
        mm.guess((1, 2, 3, 4))
        mm.guess((1, 2, 3, 4))
        mm.guess((1, 2, 3, 4))
        with self.assertRaises(MaxTriesExceeded):
            mm.guess((1, 2, 3, 4))
    
    def test_tries_left(self):
        """in progress"""
        mm = Mastermind(max_tries=3)
        self.assertEqual(mm.tries_left, 3)
        mm.guess((1, 2, 3, 4))
        self.assertEqual(mm.tries_left, 2)
    
    def test_n_try(self):
        """in progress"""
        mm = Mastermind(max_tries=3)
        self.assertEqual(mm.n_try, 0)
        mm.guess((1, 2, 3, 4))
        self.assertEqual(mm.n_try, 1)
    
    def test_max_tries(self):
        """in progress"""
        mm = Mastermind(max_tries=3)
        self.assertEqual(mm.max_tries, 3)
        mm.guess((1, 2, 3, 4))
        self.assertEqual(mm.max_tries, 3)

    def test_past(self):
        """in progress"""
        mm = Mastermind(max_tries=3)
        guess1 = tuple(reversed(mm._sequence))
        res1 = mm.guess(guess1)
        record = mm.past_sequences[0]
        self.assertEqual(record, (guess1, res1))
        guess2 = mm._sequence
        res2 = mm.guess(guess2)
        record = mm.past_sequences[0]
        self.assertEqual(record, (guess1, res1))
        record = mm.past_sequences[1]
        self.assertEqual(record, (guess2, res2))