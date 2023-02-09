import asyncio

from fastapi import FastAPI
from uvicorn import Config, Server

from game.loop import Game


class PythonBridgeSimulatorHttpServer:
    def __init__(self):
        from server.player_ship import router

        self.game = Game(server=self)

        self.app = FastAPI()
        self.app.include_router(router)
        router.server = self

        self.loop = asyncio.new_event_loop()
        self.loop.create_task(self.game.simulation.main_loop())

        config = Config(app=self.app, loop=self.loop)  # noqa
        self.server = Server(config)

    def run(self):
        print("Starting server")
        self.loop.run_until_complete(self.server.serve())
