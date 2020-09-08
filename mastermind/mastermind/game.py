import asyncio
from datetime import datetime, timedelta
from typing import List, Any

from fastapi.logger import logger
from pydantic import BaseModel

from mastermind.mongo_backend import (save_game, get_game_by_id, get_game_cursor, schedule_deletion)


class Game:
    """Abstract class representing a game instance. Concrete classes should implement
    `db_model` property which is used to serialise object for saving in db and `play` method
    with one argument, which is self documenting."""

    # TODO: `db_model` should be moved out of the class into or between mongo_backend

    def db_model(self) -> BaseModel:
        pass

    async def play(self, input: Any) -> bool:
        pass

    @classmethod
    async def get_all(cls) -> List[dict]:
        return await cls.get_games({})

    @classmethod
    async def get_games(cls, query: dict) -> List[dict]:
        cursor = get_game_cursor(query)
        logger.debug(f"Got cursor: {cursor}")
        list_game = [cls(**game) async for game in cursor]
        return list_game

    @classmethod
    async def get_game_by_id(cls, id_: str) -> dict:
        """Load a game intance from database."""
        game = await get_game_by_id(id_)
        return cls(**game)

    @classmethod
    def schedule_deletion(cls, id_: str, when: datetime) -> None:
        asyncio.create_task(schedule_deletion(id_, when))

    @classmethod
    async def new_game(cls, game_base: dict) -> dict:
        """Create a game instance and saves it to databse."""
        dict_game = cls(**game_base).serialize()
        dict_game_out = await save_game(dict_game)
        return cls(**dict_game_out)

    def __init__(self, **game_base):
        self._set_attributes = []
        logger.debug("Creating game.")
        for attr_name, value in game_base.items():
            setattr(self, attr_name, value)
            logger.debug(f"Setting attribute {attr_name} to {value}.")
            self._set_attributes.append(attr_name)
        logger.debug(f"Created: {self}.")

    def __repr__(self):
        inside = (
            f"{attr_name}={getattr(self, attr_name)}"
            for attr_name in self._set_attributes
            )
        return f"{type(self).__name__}({', '.join(inside)})"

    def serialize(self, model=None):
        if model is None:
            model = self.db_model
        logger.debug(f"Serializing model to: {model.__name__}.")
        dict_ = dict()
        for field_name in model.__fields__:
            logger.debug(f"Getting value of {field_name}.")
            try:
                value = getattr(self, field_name)
            except AttributeError:
                logger.debug(f"Value of {field_name} not set.")
                if not field_name == "id_":
                    raise
                else:
                    pass
            else:
                dict_[field_name] = value
        return dict_


class Timed(Game):
    """Mix-in. Concrete should implement `expires_at` property."""
    
    def expires_at(self) -> BaseModel:
        pass
    
    @classmethod
    async def new_game(cls, game) -> dict:
        game_out = await super().new_game(game)
        cls.schedule_deletion(game_out.id_, game_out.expires_at)
        return game_out

    @property
    def time_left(self) -> timedelta:
        datetime_now = datetime.now()
        logger.debug(f"Expires at: {self.expires_at}")
        logger.debug(f"Datetime now: {datetime_now}")
        return self.expires_at - datetime_now

class TriesLimited(Game):
    """Mix-in. Concrete should implement `n_tries` and `max_tries` property."""

    def n_tries(self) -> int:
        pass

    def max_tries(self) -> int:
        pass

    @property
    def tries_left(self) -> int:
        return self.max_tries - self.n_tries
