import asyncio
from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel
from uvicorn import Config, Server

from game.loop import Game
from game.utils import get_ship

app = FastAPI()


class ShipInstruction(BaseModel):
    module: str
    attribute: str
    value: Any

@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/ships/{ship_count}")
async def create_ships(ship_count: int):
    for i in range(0, ship_count):
        print("creating ship")
        get_ship(game.space)
    return [ship.target_angle for ship in game.space.ships]


@app.post("/set_attr")
async def set_attr(ship_instruction: ShipInstruction):
    module = getattr(game.player_ship.modules, ship_instruction.module)
    setattr(module, ship_instruction.attribute, ship_instruction.value)
    return {}

game = Game()

loop = asyncio.new_event_loop()
loop.create_task(game.main_loop())

config = Config(app=app, loop=loop)  # noqa
server = Server(config)

loop.run_until_complete(server.serve())
