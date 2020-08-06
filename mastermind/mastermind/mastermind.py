from collections import Counter, namedtuple
from enum import Enum
from itertools import compress
from random import choices
from typing import List, Sequence, Tuple

PastGuess = namedtuple("PastGuess", "guess hint")

class MaxTriesExceeded(BaseException):
    pass

class SequenceNonValid(BaseException):
    pass

class Mastermind:
    def __init__(self, n_colours=5, n_pos=4, max_tries=10):
        self._sequence = choices(range(n_colours), k=n_pos)
        self._n_colours = n_colours
        self._n_pos = n_pos
        self._max_tries = max_tries
        self._memory = []

    def guess(self, proposed_sequence: Sequence[int]) -> str:
        if self.tries_left:
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
    def n_colours(self) -> int:
        return self._n_colours

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

class GameEnded(BaseException):
    pass

class Game:

    class Status(Enum):
        NOT_STARTED = "Welcome to the game! Try guessing the sequence."
        IN_PROGRESS = "Last guess was wrong. Try again."
        SEQUENCE_NOT_VALID = "Last sequence supplied was not valid. Try again."
        WIN = "Congratulations. You won!!!."
        MAX_TRIES_EXCEEDED = "You Lose. Better luck next time!"

    def __init__(self, n_colours=5, n_pos=4, max_tries=10):
        self._game_instance = Mastermind(
            n_colours=n_colours,
            n_pos=n_pos,
            max_tries=max_tries
            )
        self._status = self.Status.NOT_STARTED

    def __repr__(self) -> str:
        return (
            f"<Game(n_colours={self._game_instance.n_colours}, "
            f"n_pos={self._game_instance.sequence_lenght}, "
            f"max_tries={self._game_instance.max_tries}): {self._status}>"
        )

    @property
    def has_ended(self) -> bool:
        return (
            self._status == self.Status.WIN
            or self._status == self.Status.MAX_TRIES_EXCEEDED
        )

    @property
    def last_game_status(self) -> Status:
        return self._status

    def guess(self, proposed_sequence: Sequence[int]):
        if self.has_ended:
            raise GameEnded
        try:
            hint = self._game_instance.guess(proposed_sequence)
        except SequenceNonValid:
            self._status = self.Status.SEQUENCE_NOT_VALID
        else:
            self._status = self.Status.IN_PROGRESS
            if hint[1] == 0 and hint[0] == self._game_instance.sequence_lenght:
                self._status = self.Status.WIN
            else:
                if self._game_instance.tries_left == 0:
                    self._status = self.Status.MAX_TRIES_EXCEEDED

    def get_history_list(self) -> List[str]:
        return [
            "|".join(str(g) for g in guess) + f": {hint}" 
            for guess, hint 
            in self._game_instance.past_sequences
            ]

    def get_history_str(self) -> str:
        lines = self.get_history_list()
        return "\n".join(lines)

    def print_message(self):
        print(self._status.value)

    def play(self):
        while True:
            self.print_message()
            if not self.has_ended:
                if past_guesses := self.get_history_str():
                    print(past_guesses)
                in_ = input()
                in_ = [int(x) for x in in_.split(" ")]
                self.guess(in_)
            else:
                break
