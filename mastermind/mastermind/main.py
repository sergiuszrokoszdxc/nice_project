from datetime import datetime, timedelta
from typing import List

from fastapi import FastAPI

from mastermind.game_provider import GameProvider
from mastermind.models import GameDetailOut, GameBase, GameToList, Guess

# TODO: add validation
    # TODO: websockets
    # TODO: add pagination

app = FastAPI()

games = GameProvider()

@app.get("/game", response_model=List[GameToList])
async def get_game():
    games_list = await games.get_all()
    return games_list

@app.post("/game", response_model=GameToList)
async def post_game(game: GameBase):
    expires_at = datetime.now() + timedelta("30 min")
    game_in = game.dict()
    game_out = games.create_game(**game_in, expires_at=expires_at)
    return game_out

@app.get("/game/{game_id}", response_model=GameDetailOut)
async def get_guess(game_id: str):
    game = games.get_game_by_id(game_id)
    return game

@app.post("/game/{game_id}", response_model=GameDetailOut)
async def post_guess(game_id: str, guess: Guess):
    game_dict = games.guess(game_id, guess["guess"])
    return game_dict
