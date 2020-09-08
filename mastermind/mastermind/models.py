from datetime import datetime, timedelta
from typing import List, Tuple

from pydantic import BaseModel, conint, validator

PosInt = conint(ge=1, strict=True)
NonNegInt = conint(ge=0, strict=True)

class MastermindBaseSpec(BaseModel):
    n_colours: PosInt
    n_positions: PosInt
    max_tries: PosInt

class Guess(BaseModel):
    guess: Tuple[NonNegInt, ...]

class GuessHint(Guess):
    hint: Tuple[NonNegInt, NonNegInt]

class MastermindDBIn(MastermindBaseSpec):
    id_: str = None
    sequence: Tuple[NonNegInt, ...]
    expires_at: datetime
    history: List[GuessHint] = []
    class Config:
        orm_mode = True

class MastermindSumm(MastermindBaseSpec):
    id_: str
    tries_left: int
    time_left: timedelta
    has_ended: bool

class MastermindDetail(MastermindSumm):
    history: List[GuessHint]

class MastermindResult(MastermindDetail):
    win_token: bool
