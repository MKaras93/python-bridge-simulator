from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

import pygame
import pymunk
import pymunk.pygame_util

from .scenarios import ACTIVE_SCENARIO
from .hyperspace import HyperSpace

if TYPE_CHECKING:
    from typing import Optional
    from game.player_ship import PlayerShip

class Game:
    @staticmethod
    def _get_space() -> HyperSpace:
        space = HyperSpace()
        space.gravity = 0, 0
        space.damping = 0.2
        return space

    def __init__(self):
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
