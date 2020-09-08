from collections import Counter
from datetime import datetime, timedelta
from itertools import compress
from random import choices
from typing import Tuple

from fastapi.logger import logger

from mastermind.game import Timed, TriesLimited
from mastermind.models import MastermindDBIn
from mastermind.mongo_backend import update_game

class Mastermind(Timed, TriesLimited):

    db_model = MastermindDBIn

    def __init__(self, **game_base):
        n_colours = game_base["n_colours"]
        n_positions = game_base["n_positions"]
        if "sequence" not in game_base:
            game_base["sequence"] = choices(range(n_colours), k=n_positions)
            game_base["history"] = []
        super().__init__(**game_base)

    @property
    def n_tries(self) -> int:
        return len(self.history) # pylint: disable=no-member

    @property
    def has_ended(self):
        try:
            last = self.history[-1] # pylint: disable=no-member
        except IndexError:
            won = False
        else:
            hint = last["hint"]
            won = self._if_win(hint)
        return bool(not (self.max_tries - self.n_tries > 0) or won)
    
    def _if_win(self, hint):
        return hint[0] == self.n_positions # pylint: disable=no-member

    async def play(self, input_: Tuple[int]) -> bool:
        """Try to guess the sequence."""
        if not self.has_ended:
            hint = self._guess(input_)
            result = {"guess": input_, "hint": hint}
            await self._save_guess_result(result)
            if self._if_win(hint):
                win = True
                time_offset = datetime.now() + timedelta(minutes=3)
                try:
                    id_ = self.id_
                except AttributeError:
                    logger.debug(f"{self} not yet saved in database.")
                else:
                    self.schedule_deletion(id_, time_offset) # pylint: disable=no-member
            else:
                win = False
        else:
            win = False
        return win

    def _guess(self, proposed_sequence: Tuple[int]) -> Tuple[int]:
        correct_mask = tuple(
            x == y
            for x, y in zip(proposed_sequence, self.sequence) # pylint: disable=no-member
            )
        wrong_mask = tuple(not x for x in correct_mask)
        n_correct_pos = sum(correct_mask)
        # count unmatched pins by colour in both sequences
        wrong_pins = Counter(compress(proposed_sequence, wrong_mask))
        umatched_pins = Counter(compress(self.sequence, wrong_mask)) # pylint: disable=no-member
        # in leftover pins check how many pins are matched by colour
        # between both groups
        correct_colours_by_colour = (
            min(count, wrong_pins.get(colour, 0))
            for colour, count in umatched_pins.items()
            )
        n_correct_col = sum(correct_colours_by_colour)\

        return n_correct_pos, n_correct_col

    async def _save_guess_result(self, result: dict) -> None:
        self.history.append(result) # pylint: disable=no-member
        await update_game(self.serialize())
