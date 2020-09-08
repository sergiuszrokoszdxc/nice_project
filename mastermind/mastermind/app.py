import asyncio
import random
from typing import Optional, List

from fastapi import FastAPI, Form, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from mastermind.mastermind import Game

# TODO: MAKE IT SO IT IS AVAILABLE ONLY LIMITED AMOUNT OF TIME

app = FastAPI()

templates = Jinja2Templates(directory='mastermind/templates')

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

game = Game(n_colours=5, n_pos=4, max_tries=10)

msg_alternatives = {
    Game.Status.WIN: "Congratulations! You won. How about next game?",
    Game.Status.MAX_TRIES_EXCEEDED: "You Lose. How about next game?",
}

@app.get("/test")
async def get_test():
    global game
    status = game.last_game_status
    msg = status.value
    if game.has_ended:
        game = Game(n_colours=5, n_pos=4, max_tries=10)
        msg = msg_alternatives[status]
        history = []
    else:
        history = game.past_sequences
    return {
        "history": history,
        "msg": msg
        }
       

@app.post("/test")
async def post_test(guess: List[int]):
    game.guess(guess)
    return {}
