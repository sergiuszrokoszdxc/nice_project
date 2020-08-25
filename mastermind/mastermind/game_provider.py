import asyncio
from datetime import datetime, timedelta
from random import choices
from typing import List, Tuple

from mastermind.mastermind import CorrectSequence, Mastermind, MaxTriesExceeded
from mastermind.mongo_backend import (create_game_doc, retrieve_game_by_id, 
                                      get_game_cursor, postpone_deletion, Memory)

class GameProvider:

    @classmethod
    async def create_game(
        cls,
        n_colours: int,
        n_positions: int,
        max_tries: int,
        expires_at: datetime
    ) -> dict:
        """Create a game instance and saves it to databse."""
        sequence = choices(range(n_colours), k=n_positions)
        game = await create_game_doc(n_colours, sequence, max_tries, expires_at)
        cls._extend_dict(game)
        _id = game["_id"]
        cls._schedule_deletion(_id, expires_at)
        return game

    async def get_game_by_id(self, _id: str) -> dict:
        """Load a game intance from database."""
        game = await retrieve_game_by_id(_id)
        self._extend_dict(game)
        return game

    async def get_games(self, query: dict) -> List[dict]:
        cursor = get_game_cursor(query)
        game_list = [self._extend_dict(game) async for game in cursor]
        return game_list
    
    async def get_all(self) -> List[dict]:
        return await self.get_games({})

    async def guess(self, _id: str, guess: Tuple[int]) -> dict:
        game = await self.get_game_by_id(_id)
        self._extend_dict(game)
        game_obj = self._create_game_obj(game)
        try:
            await game_obj.guess(guess["guess"])
        except MaxTriesExceeded:
            win_token = False
        except CorrectSequence:
            win_token = True
        else:
            win_token = False
        game_dict = self._create_game_dict(game_obj, game["_id"], game["has_ended"])
        game_dict["win_token"] = win_token
        return game_dict
    
    @staticmethod
    def _extend_dict(game_dict: dict) -> dict:
        n_tries = len(game_dict["memory"])
        game_dict["tries_left"] = game_dict["max_tries"] - n_tries
        game_dict["time_left"] = game_dict["expires_at"] - datetime.now()
        already_won = game_dict["memory"][-1]["hint"] == game_dict["n_positions"]
        game_dict["has_ended"] = (not game_dict["tries_left"]) and (not already_won)

    @staticmethod
    def _schedule_deletion(_id: str, expires_at: datetime) -> None:
        asyncio.create_task(postpone_deletion(_id, expires_at))

    def _create_game_obj(self, game: dict) -> Mastermind:
        n_colours = game["n_colours"]
        max_tries = game["max_tries"]
        expires_at = game["expires_at"]
        memory = Memory(game["_id"], game["memory"])
        sequence = game["sequence"]
        return Mastermind(n_colours, max_tries, expires_at, memory, sequence)

    def _create_game_dict(self, game: Mastermind, _id, has_ended) -> dict:
        return {        
            "n_colours": game.n_colours,
            "n_positions": game.n_positions,
            "max_tries": game.max_tries,
            "_id": _id,
            "tries_left": game.tries_left,
            "time_left": game.expires_at - datetime.now(),
            "has_ended": has_ended,
            "past_results": game.memory,
        }
