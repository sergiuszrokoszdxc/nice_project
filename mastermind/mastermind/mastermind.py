from collections import Counter
from datetime import datetime, timedelta
from itertools import compress
from typing import Tuple

from mastermind.mongo_backend import Memory

class GameEnding(BaseException):
    """The game is going to stop."""

class MaxTriesExceeded(GameEnding):
    """Max number of tries exceeded for this game."""

class CorrectSequence(GameEnding):
    """The game is ending as correct sequence was supplied."""

class Mastermind:

    def __init__(
        self,
        n_colours: int,
        max_tries: int,
        expires_at: datetime,
        memory: Memory,
        sequence: Tuple[int],
    ):
        self.n_colours = n_colours
        self.n_positions = len(sequence)
        self.max_tries = max_tries
        self.expires_at = expires_at
        self.memory = memory
        self.sequence = sequence

    @property
    def tries_left(self) -> int:
        return self.max_tries - self.n_try

    @property
    def n_try(self) -> int:
        return len(self.memory)

    async def guess(self, sequence: Tuple[int]) -> Tuple[int]:
        """Try to guess the sequence."""
        if self.tries_left:
            hint = self._guess(sequence)
            result = {"guess": sequence, "hint": hint}
            await self._save_guess_result(result)
            if hint[0] == self.n_positions:
                raise CorrectSequence
            return hint
        else:
            raise MaxTriesExceeded

    def _guess(self, proposed_sequence: Tuple[int]) -> Tuple[int]:
        correct_mask = tuple(
            x == y
            for x, y in zip(proposed_sequence, self.sequence)
            )
        wrong_mask = tuple(not x for x in correct_mask)
        n_correct_pos = sum(correct_mask)
        # count unmatched pins by colour in both sequences
        wrong_pins = Counter(compress(proposed_sequence, wrong_mask))
        umatched_pins = Counter(compress(self.sequence, wrong_mask))
        # in leftover pins check how many pins are matched by colour
        # between both groups
        correct_colours_by_colour = (
            min(count, wrong_pins.get(colour, 0))
            for colour, count in umatched_pins.items()
            )
        n_correct_col = sum(correct_colours_by_colour)

        assert n_correct_pos + n_correct_col == self.n_positions

        return n_correct_pos, n_correct_col

    async def _save_guess_result(self, result: Tuple[int]) -> None:
        await self.memory.append(
            result,
            self.n_colours,
            self.n_positions,
            self.max_tries,
            self.expires_at,
            self.sequence
            )
