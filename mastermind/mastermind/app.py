from mastermind.mastermind import Game

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

import asyncio
# TODO: MAKE IT SO IT IS AVAILABLE ONLY LIMITED AMOUNT OF TIME


app = FastAPI()

templates = Jinja2Templates(directory='templates')

game = Game()

@app.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    history = game.get_history()
    tries_left = game.game_instance.tries_left
    return templates.TemplateResponse(
        "item.html",
        {"request": request, "history": history, "tries_left": tries_left}
        )

@app.post("/"):
async def post_index(request: Request, seq: List[int]: Form(...)):
    game.guess(seq)
    return RedirectResponse(request.url_for("get_index"))
