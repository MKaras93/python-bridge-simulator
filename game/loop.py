import asyncio
import random
from typing import List

import pygame
import pymunk
import pymunk.pygame_util
from pymunk import Vec2d

from .hyperspace import HyperSpace, HyperspaceShip
from .utils import get_ship, create_circle_for_body


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
        pygame.init()

        # debug
        self._fill_space()

    def _fill_space(self):
        """
        Debug function, used to speed things up. If you want something to happen on space start up - do it here.
        """
        self.space.ships = [get_ship(self.space) for i in range(0, 4)]
        # self.ship = get_ship(self.space)

        #
        # self.target_x = self.ship.body.position.x + random.randint(-100, 100)
        # self.target_y = self.ship.body.position.y + random.randint(-100, 100)
        # self.space.create_ship((self.target_x, self.target_y))

    def update(self, dt: float):
        self.ct += 1
        self.space.step(dt)
        self.space.tick()

        if self.ct % 50 == 0:
            _set_random_target_angle_for_ships(self.space.ships)

        # _fly_to_point(self.ship, self.target_x, self.target_y)

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


# utils


def _set_random_target_angle_for_ships(ships: List[HyperspaceShip]):
    for ship in ships:
        new_value = random.randint(0, 360)
        print(f"setting new target angle to {new_value}. Current angle: {ship.angle}.")
        ship.target_angle = new_value


def _fly_to_point(ship: HyperspaceShip, target_x, target_y):
    ship.rotation_engine_percent = 0
    ship.engine_percent = 0
    angle = ship.body.position.get_angle_degrees_between(Vec2d(target_x, target_y))
    print("angle:", angle)
    ship.target_angle = ship.angle - angle
    if ship.target_angle:
        ship.rotation_engine_percent = 50

    if ship.angle - ship.target_angle < 5:
        ship.rotation_engine_percent = 0
        distance = ship.body.position.get_distance((target_x, target_y))
        print("distance to target:", distance)
        ship.engine_percent = distance
        if distance <= 10:
            print("Target in sight!")
