from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import FastAPI
from uvicorn import Config, Server

from server.base_class import BasePythonBridgeSimulatorServer

if TYPE_CHECKING:
    from game.loop import Game
    from asyncio import AbstractEventLoop


class PythonBridgeSimulatorHttpServer(BasePythonBridgeSimulatorServer):
    def __init__(self, game: Game, loop: AbstractEventLoop):
        from server.fast_api_server.endpoints import router

        super().__init__(game, loop)

        self.app = FastAPI()
        self.app.include_router(router)
        router.server = self  # TODO: ugly solution to circular import problem - consider redesigning modules structure

        config = Config(app=self.app, loop=loop, timeout_keep_alive=60)  # noqa
        self.server = Server(config)

    async def run(self):
        await super().run()
        await self.server.serve()
