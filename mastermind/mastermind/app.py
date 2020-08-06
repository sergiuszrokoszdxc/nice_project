from mastermind.mastermind import Game

from fastapi import FastAPI, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

import asyncio
# TODO: MAKE IT SO IT IS AVAILABLE ONLY LIMITED AMOUNT OF TIME


app = FastAPI()

templates = Jinja2Templates(directory='templates')

game = Game(n_colours=5, n_pos=4, max_tries=10)

msg_alternatives = {
    Game.Status.WIN: "Congratulations! You won. How about next game?",
    Game.Status.MAX_TRIES_EXCEEDED: "You Lose. How about next game?",
}

@app.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    global game
    status = game.last_game_status
    msg = status.value
    if game.has_ended:
        game = Game(n_colours=5, n_pos=4, max_tries=10)
        msg = msg_alternatives[status]
        history = []
    else:
        history = game.get_history_list()
    return templates.TemplateResponse(
        "item.html",
        {
            "request": request,
            "msg": msg,
            "history": history
        }
    )

        
@app.post("/")
async def post_index(
    request: Request,
    first: int = Form(None, ge=0, le=4),
    second: int = Form(None, ge=0, le=4),
    third: int = Form(None, ge=0, le=4),
    fourth: int = Form(None, ge=0, le=4),
):
    seq = []
    for el in [first, second, third, fourth]:
        if el:
            seq.append(el)
    game.guess(seq)
    return RedirectResponse(
        request.url_for("get_index"),
        status_code=status.HTTP_303_SEE_OTHER
    )
