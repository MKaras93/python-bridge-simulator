import asyncio

from fastapi import FastAPI
from uvicorn import Config, Server

from server.player_ship import router
from server.game_objects import game

app = FastAPI()
app.include_router(router)

loop = asyncio.new_event_loop()
loop.create_task(game.simulation.main_loop())

config = Config(app=app, loop=loop)  # noqa
server = Server(config)

loop.run_until_complete(server.serve())
