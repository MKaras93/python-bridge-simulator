# Main file responsible for running both game and server asynchronously.

import asyncio

from game.core import Game
from server.fast_api_server.fast_api_server import PythonBridgeSimulatorHttpServer

SERVER_CLASS = PythonBridgeSimulatorHttpServer  # If you want to use a different server class, use it here.

loop = asyncio.new_event_loop()
game = Game()

# scheduling main game loop
loop.create_task(game.simulation.main_loop())

server = SERVER_CLASS(game=game, loop=loop)

# scheduling and running server
loop.run_until_complete(server.run())
