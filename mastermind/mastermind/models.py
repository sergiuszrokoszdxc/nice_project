from datetime import datetime, timedelta
from typing import List, Tuple

from pydantic import BaseModel

class GameBase(BaseModel):
    n_colours: int
    n_positions: int
    max_tries: int

class Guess(BaseModel):
    guess: Tuple[int]

class Result(BaseModel):
    guess: Guess
    hint: tuple

class GameToList(GameBase):
    _id: str
    tries_left: int
    time_left: timedelta
    has_ended: bool

class GameDetail(GameToList):
    past_results: List[Result]

class GameDetailOut(GameDetail):
    win_token: bool