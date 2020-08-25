import asyncio
from datetime import datetime
from typing import Tuple

import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient("mongo", 27017)

backend = client["app_database"]

games = backend["games_collection"]
# TODO: add logging

async def create_game_doc(
    n_colours: int,
    sequence: Tuple[int],
    max_tries: int,
    expires_at: datetime
) -> dict:
    document = {
        "n_colours": n_colours,
        "n_positions": len(sequence),
        "max_tries": max_tries,
        "expires_at": expires_at,
        "sequence": sequence,
        "history": []
    }
    result = await games.insert_one(document)
    document["_id"] = result.inserted_id
    return document

def get_game_cursor(query):
    cursor = games.find(query)
    return cursor

async def retrieve_game_by_id(_id: str) -> dict:
    game = await games.find_one({"_id": _id})
    return game

async def postpone_deletion(_id: str, expires_at: datetime) -> None:
    postpone_timedelta = expires_at - datetime.now()
    asyncio.sleep(postpone_timedelta)
    await games.delete_one({"_id": _id})


class Memory:
    def __init__(self, _id, memory):
        self.memory = memory
        self._id = _id

    def __len__(self) -> int:
        return len(self.memory)
    
    async def append(
        self,
        result: tuple,
        n_colours: int,
        n_positions :int,
        max_tries: int,
        expires_at : datetime,
        sequence: Tuple[int]
    ) -> None:
        self.memory.append(result)
        new_document = {
            "n_colours": n_colours,
            "n_positions": n_positions,
            "max_tries": max_tries,
            "expires_at": expires_at,
            "sequence": sequence,
            "history": self.memory
        }
        result = await games.replace_one({"_id": self._id}, new_document)
        assert result.modified_count == 1
