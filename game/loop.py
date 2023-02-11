from __future__ import annotations

import asyncio
import datetime
from typing import TYPE_CHECKING

import pygame
import pymunk
import pymunk.pygame_util

from .hyperspace import HyperSpace
from .scenarios import ACTIVE_SCENARIO

if TYPE_CHECKING:
    from typing import Optional, Any
    from game.player_ship import PlayerShip
    from server.base_class import BasePythonBridgeSimulatorServer
    from .ship_modules import ShipModule


class Simulation:
    @staticmethod
    def _get_space() -> HyperSpace:
        space = HyperSpace()
        space.gravity = 0, 0
        space.damping = 0.2
        return space

    def __init__(self, game: Game):
        self.game: Game = game
        self.space: HyperSpace = self._get_space()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((1000, 700))
        self.options = pymunk.pygame_util.DrawOptions(self.screen)
        self.ct = 0
        self.player_ship: Optional[PlayerShip] = None
        self.scenario = ACTIVE_SCENARIO(self)
        pygame.init()

    def update(self, dt: float):
        self.ct += 1
        if self.scenario:
            self.scenario.play(self.ct)
        self.space.step(dt)
        self.space.tick()

    async def main_loop(self):
        while True:
            await asyncio.sleep(0)
            t = self.clock.tick(20) / 1000
            self.update(round(t, 1))
            pygame.display.flip()
            self.screen.fill((0, 0, 0))
            self.space.debug_draw(self.options)
            for event in pygame.event.get():
                if (
                        event.type == pygame.QUIT
                        or event.type == pygame.KEYDOWN
                        and (event.key in [pygame.K_ESCAPE, pygame.K_q])
                ):
                    print("Game Over!")
                    quit()


class Game:
    """
    Main class wrapping the whole game, simulation etc.
    It exposes interface which the Server class can use to interact with the game.
    """

    def __init__(self):
        self.server: Optional[BasePythonBridgeSimulatorServer] = None
        self.simulation = Simulation(self)

    def attach_server(self, server):
        print(f"Attaching game to {server}")
        self.server = server

    def get_attribute(self, user_name: str, module_name: str, attribute_name: str):
        self.simulation.player_ship.modules.validate_module_name(module_name)
        module: ShipModule = getattr(self.simulation.player_ship.modules, module_name)
        self._check_permission(module, user_name)
        return module.get_attribute(attribute_name)

    def set_attribute(self, user_name: str, module_name: str, attribute_name: str, value: Any):
        self.simulation.player_ship.modules.validate_module_name(module_name)
        module: ShipModule = getattr(self.simulation.player_ship.modules, module_name)
        self._check_permission(module, user_name)
        return module.set_attribute(attribute_name, value)

    def call_method(self, user_name: str, module_name: str, method_name: str, **kwargs):
        self.simulation.player_ship.modules.validate_module_name(module_name)
        module: ShipModule = getattr(self.simulation.player_ship.modules, module_name)
        self._check_permission(module, user_name)
        return module.call_method(method_name, **kwargs)

    def log(self, level: str, message: str, module_name: str = "", module: ShipModule = None):
        if module_name:  # Either module or module_name is required. They can't be provided together.
            if module:
                raise ValueError("You have to provide either 'module' or 'module_name' parameters, not both.")
            module: ShipModule = getattr(self.simulation.player_ship.modules, module_name)
        elif not module:
            raise ValueError("Either 'module' or 'module_name' must be provided.")

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for user in module.operators:
            self.server.log(module.module_type, level, message, user, timestamp)
        print(f"[{timestamp}][{level}][{module_name.upper()}]: {message}")

    @staticmethod
    def _check_permission(module: ShipModule, user_name: str) -> bool:
        return user_name in module.operators
