import asyncio
import hashlib
import random
from typing import Optional, List

from fastapi import Depends, FastAPI, Form, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from mastermind.mastermind import Mastermind, MaxTriesExceeded

# TODO: MAKE IT SO IT IS AVAILABLE ONLY LIMITED AMOUNT OF TIME
# TODO: timing
# TODO: garbage_collect old games
# TODO: unique id for any game disregarding parameters
# TODO:

app = FastAPI()

origins = [
    "http://localhost:3000/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

games = dict()

games["1"] = [Mastermind(), False]
games["2"] = [Mastermind(2,2,3), False]
games["3"] = [Mastermind(2,2,3), False]

games["1"][0].guess([1,2,1,1])
games["1"][0].guess([1,2,1,1])
games["1"][0].guess([1,2,1,1])
games["1"][0].guess([1,2,1,1])
games["2"][1] = True

class Game(BaseModel):
    n_colours: int
    n_positions: int
    max_tries: int

class GameOut(BaseModel):
    id_: str
    n_colours: int
    n_positions: int
    max_tries: int
    has_ended: bool


@app.get("/game", response_model=List[GameOut])
async def get_game():
    # websockets
    # add pagination
    global games
    games_list = [
        {
            "id_": id_,
            "n_colours": game.n_colours,
            "n_positions": game.n_positions,
            "max_tries": game.max_tries,
            "has_ended": has_ended
        }
        for id_, (game, has_ended) in games.items()
    ]
    print(games_list)
    return games_list

@app.post("/game", response_model=GameOut)
async def post_game(game: Game):
    global games
    id_ = hashlib.sha1(game.json(sort_keys=True)).hexdigest()
    m = Mastermind(**game.dict())
    games[id_] = [game, False]
    game_out = GameOut(id_=id_, has_ended=False, **game.dict())
    return game_out

@app.get("/game/{game_id}")
async def get_guess(game_id: str):
    global games
    game, has_ended = games[game_id]
    history = game.past_sequences
    return {
        # game
        "has_ended": has_ended,
        "history": history,
        "win_token": False
        }
       

@app.post("/game/{game_id}")
async def post_guess(game_id: str, guess: List[int]):
    global games
    game, has_ended = games[game_id]
    if not has_ended:
        try:
            hint = game.guess(guess)
        except MaxTriesExceeded:
            win_token = False
            has_ended = True
        else:
            if hint[1] == 0 and hint[0] == game.n_positions:
                win_token = True
                has_ended = True
                games[game_id] = game, has_ended
            else:
                win_token = False
                if game.tries_left == 0:
                    has_ended = True
                    games[game_id] = game, has_ended
    else:
        win_token = False
    history = game.past_sequences
    return {
        # game,
        "has_ended": has_ended,
        "history": history,
        "win_token": win_token
    }
