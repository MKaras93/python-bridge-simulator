from __future__ import annotations

import abc
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.loop import Game
    from asyncio import AbstractEventLoop


class BasePythonBridgeSimulatorServer(abc.ABC):
    def __init__(self, game: Game, loop: AbstractEventLoop):
        """
        PythonBridgeSimulatorServer concrete classes must run super().__init__.
        Afterwards they should do whatever they need to be ready to call the 'run' method.
        """
        print(f"Initializing {self.__class__.__name__}")
        self.game = game
        self.game.attach_server(self)
        self.loop = loop

    async def run(self):
        """
        Run method of the concrete class should run the asynchronous server.
        """
        print("Starting server")
