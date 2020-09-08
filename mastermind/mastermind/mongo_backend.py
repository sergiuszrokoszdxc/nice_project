import asyncio
from datetime import datetime
import logging
import os

from bson.objectid import ObjectId
from fastapi.logger import logger
import motor.motor_asyncio

# TODO: turn into BaseSetting from Pydantic
MONGO_HOST = os.environ.get("MONGO_HOST")
MONGO_PORT = int(os.environ.get("MONGO_PORT"))

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_HOST, MONGO_PORT)

backend = client["app_database"]

games_collection = backend["games_collection"]

async def save_game(game_in: dict) -> dict:
    result = await games_collection.insert_one(game_in)
    game_out = dict(game_in)
    game_out["id_"] = str(result.inserted_id)
    logger.info(f"Saved: {game_out}.")
    return game_out

async def update_game(game_in: dict) -> None:
    _id = ObjectId(game_in["id_"])
    await games_collection.replace_one({"_id": _id}, game_in)
    logger.info(f"Updated: {game_in}.")

async def schedule_deletion(id_: str, when: datetime) -> None:
    postpone_timedelta = when - datetime.now()
    logger.debug(
        f"Scheduled for deletion in {postpone_timedelta.total_seconds()} seconds id: {id_}."
        )
    await asyncio.sleep(postpone_timedelta.total_seconds())
    _id = ObjectId(id_)
    await games_collection.delete_one({"_id": _id})
    logger.info(f"Deleted id: {id_}.")

async def get_game_by_id(id_: str) -> dict:
    _id = ObjectId(id_)
    game_out = await games_collection.find_one({"_id": _id})
    logger.info(f"Found: {game_out}.")
    game_out["id_"] = id_
    return game_out

async def get_game_cursor(query):
    cursor = games_collection.find(query)
    async for game in cursor:
        logger.info(f"Found: {game}.")
        game["id_"] = str(game["_id"])
        yield game
