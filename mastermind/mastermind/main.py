from datetime import datetime, timedelta
import logging
from typing import List

from fastapi import FastAPI
from fastapi.logger import logger

from mastermind.mastermind import Mastermind
from mastermind.models import (Guess, MastermindBaseSpec, MastermindDetail,
                               MastermindSumm, MastermindResult)

# TODO: add tests
# TODO: add proper type annotations
# TODO: add configuration from venv
# TODO: add venv to change logging level
# TODO: port to kubernetes
# TODO: add `once more` button

# ======================================

# TODO: add logging
# TODO: websockets
# TODO: add pagination


app = FastAPI()


gunicorn_logger = logging.getLogger("gunicorn.error")
logger.handlers = gunicorn_logger.handlers
logger.setLevel(gunicorn_logger.level)

@app.get("/game", response_model=List[MastermindSumm])
async def get_game():
    logger.debug("Getting list of all games.")
    games_list = await Mastermind.get_all()
    games_list = [game.serialize(MastermindSumm) for game in games_list]
    return games_list

@app.post("/game", response_model=MastermindSumm)
async def post_game(new_game: MastermindBaseSpec):
    game_base = new_game.dict()
    game_base["expires_at"] = datetime.now() + timedelta(minutes=30)
    game = await Mastermind.new_game(game_base)
    game = game.serialize(MastermindSumm)
    return game

@app.get("/game/{game_id}", response_model=MastermindDetail)
async def get_guess(game_id: str):
    game = await Mastermind.get_game_by_id(game_id)
    game = game.serialize(MastermindDetail)
    return game

@app.post("/game/{game_id}", response_model=MastermindResult)
async def post_guess(game_id: str, guess: Guess):
    game = await Mastermind.get_game_by_id(game_id)
    # TODO: should check for guess validity against n_colours and n_positions
    win = await game.play(guess.guess)
    game_result = game.serialize(MastermindDetail)
    game_result["win_token"] = win
    return game_result
