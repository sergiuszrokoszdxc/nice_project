import unittest

from mastermind.mastermind import Game, GameEnded


class TestMastermind(unittest.TestCase):

    def test_win(self):
        """Able to win."""
        g = Game()
        self.assertEqual(g.Status.NOT_STARTED, g.last_game_status)
        seq = g._game_instance._sequence
        g.guess(seq)
        self.assertEqual(g.Status.WIN, g.last_game_status)

    def test_lose(self):
        """Max tries exceeded."""
        g = Game(n_colours=3, max_tries=3)
        self.assertEqual(g.Status.NOT_STARTED, g.last_game_status)
        seq = list(g._game_instance._sequence)
        seq[0] = (seq[0] + 1) % 3
        g.guess(seq)
        self.assertEqual(g.Status.IN_PROGRESS, g.last_game_status)
        g.guess(seq)
        g.guess(seq)
        self.assertEqual(g.Status.MAX_TRIES_EXCEEDED, g.last_game_status)
        with self.assertRaises(GameEnded):
            g.guess(seq)

    def test_non_valid(self):
        """Non valid guess."""
        g = Game()
        self.assertEqual(g.Status.NOT_STARTED, g.last_game_status)
        seq = g._game_instance._sequence
        seq.append(1)
        g.guess(seq)
        self.assertEqual(g.Status.SEQUENCE_NOT_VALID, g.last_game_status)

    def test_configuration(self):
        """Check config."""
        g = Game(n_colours=10, n_pos=8, max_tries=20)
        self.assertEqual(10, g._game_instance.n_colours)
        self.assertEqual(8, g._game_instance.sequence_lenght)
        self.assertEqual(20, g._game_instance.max_tries)
