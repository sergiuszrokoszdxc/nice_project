from collections import Counter, namedtuple
from enum import Enum
from itertools import compress
from random import sample
from typing import List, Sequence, Tuple

PastGuess = namedtuple("PastGuess", "guess hint")

class MaxTriesExceeded(BaseException):
    pass

class SequenceNonValid(BaseException):
    pass

class Mastermind:
    def __init__(self, n_colours=5, n_pos=4, max_tries=10):
        self._sequence = sample(range(n_colours), n_pos)
        self._n_colours = n_colours
        self._n_pos = n_pos
        self._max_tries = max_tries
        self._memory = []

    def guess(self, proposed_sequence: Sequence[int]) -> str:
        if self.n_try < self._max_tries:
            # if not valid exception is raised
            self._validate(proposed_sequence)
            hint = self._guess(proposed_sequence)
            record = PastGuess(proposed_sequence, hint)
            self._memory.append(record)
            return hint
        else:
            raise MaxTriesExceeded

    @property
    def tries_left(self) -> int:
        return self._max_tries - self.n_try

    @property
    def n_try(self) -> int:
        return len(self._memory)

    @property
    def max_tries(self) -> int:
        return self._max_tries

    @property
    def past_sequences(self) -> List[PastGuess]:
        return self._memory

    @property
    def sequence_lenght(self) -> int:
        return self._n_pos

    def _validate(self, sequence: Sequence[int]) -> None:
        # proposed sequence needs to have proper length
        # and consists of proper numbers
        valid = len(sequence) == self._n_pos \
            and min(sequence) >= 0 \
            and max(sequence) < self._n_colours
        # TODO: sequence validation results could be added
        if not valid:
            raise SequenceNonValid
    
    def _guess(self, proposed_sequence: Sequence[int]) -> Tuple[int]:
        correct_mask = tuple(
            x == y
            for x, y in zip(proposed_sequence, self._sequence)
            )
        wrong_mask = tuple(not x for x in correct_mask)
        n_correct_pos = sum(correct_mask)
        # count unmatched pins by colour in both sequences
        wrong_pins = Counter(compress(proposed_sequence, wrong_mask))
        umatched_pins = Counter(compress(self._sequence, wrong_mask))
        # in leftover pins check how many pins are matched by colour
        # between both groups
        correct_colours_by_colour = (
            min(count, wrong_pins.get(colour, 0))
            for colour, count in umatched_pins.items()
            )
        n_correct_col = sum(correct_colours_by_colour)

        return n_correct_pos, n_correct_col


class Game:

    class Status(Enum):
        NOT_STARTED = "Game not yet started."
        IN_PROGRESS = ""
        SEQUENCE_NOT_VALID = ""
        WIN = "Sequence supplied is not valid."
        MAX_TRIES_EXCEEDED = ""

    def __init__(self, n_colours=5, n_pos=4, max_tries=10):
        self.game_instance = Mastermind(n_colours=5, n_pos=4, max_tries=10)
        self.status = Status.NOT_STARTED

    def guess(self, proposed_sequence: Sequence[int]) -> str:
        try:
            hint = self.game_instance.guess(proposed_sequence)
        except SequenceNonValid:
            self.status = Status.SEQUENCE_NOT_VALID
        else:
            self.status = Status.IN_PROGRESS
            if hint[1] == 0 and hint[0] == self.game_instance.sequence_lenght:
                self.status = Status.WIN
            else:
                self.msg = f"Pins in good position: {hint[0]}. Pins in good colour: {hint[1]}."
                if self.game_instance.tries_left == 0:
                    self.status = Status.MAX_TRIES_EXCEEDED
                    msg += "\n All tries used. You lose."
        return msg

    def get_history(self) -> str:
        lines = ["|".join(str(g) for g in guess) + f": {hint}" for guess, hint in self.game_instance.past_sequences]
        return "\n".join(lines)

    def play(self):
        while True:
            in_ = input()
            in_ = [int(x) for x in in_.split(" ")]
            try:
                print(self.guess(in_))
            except MaxTriesExceeded:
                self.game_instance = Mastermind(n_colours=5, n_pos=4, max_tries=10)
            else:
                print(self.get_history())

