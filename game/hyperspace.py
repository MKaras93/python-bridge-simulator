from __future__ import annotations

import datetime
import typing
from enum import Enum

import math
import pymunk
from pymunk import Vec2d

from .utils import (
    clockwise_degrees_to_anti_clockwise_radian,
    anticlockwise_radian_to_clockwise_degrees,
    get_sector_coords,
)

if typing.TYPE_CHECKING:
    from .internal_ship.classes import InternalShip
    from typing import Tuple, List, Optional


class Hyperspace(pymunk.Space):
    def __init__(self, threaded=False):
        super().__init__(threaded=threaded)
        self.ships: List[HyperspaceShip] = []

    def tick(self):
        for ship in self.ships:
            ship.tick()


class HyperspaceShip:
    def __init__(self, internal_ship: InternalShip, position: Vec2d):
        self.internal_ship: InternalShip = internal_ship
        self.space: Hyperspace = internal_ship.space

        self.body = pymunk.Body(body_type=pymunk.Body.DYNAMIC, mass=1, moment=1)
        self._circle = pymunk.Circle(self.body, radius=10)
        self.space.add(self.body)
        self.space.add(self._circle)
        self.space.ships.append(self)
        self.body.position = position

        self.sector: Optional[Sector] = None

    @property
    def angle(self) -> float:
        return anticlockwise_radian_to_clockwise_degrees(self.body.angle)

    @angle.setter
    def angle(self, value: int):
        self.body.angle = clockwise_degrees_to_anti_clockwise_radian(value)

    def _cut_off_engine(self):
        self.internal_ship.engine_percent = 0
        self.internal_ship.engine_cut_off_time = None

    def _add_engine_force(self):
        if self.internal_ship.engine_percent == 0:
            return
        else:
            speed = self.internal_ship.engine_percent / 100 * self.internal_ship.engine_power
            force_vector = Vec2d(speed, 0)
            self.body.apply_force_at_local_point(force_vector)

        if self.internal_ship.engine_cut_off_time is not None:
            now = datetime.datetime.now()
            if now >= self.internal_ship.engine_cut_off_time:
                self._cut_off_engine()

    def _rotate(self):
        # TODO: Change. With this logic the ship has a constant turn it makes per frame. If this turn is bigger than the
        # angular_diff - it will miss the target_angle and fall into infinite loop.

        if self.internal_ship.target_angle is None:
            return

        angular_diff = self.internal_ship.target_angle - self.angle
        if abs(angular_diff) <= 1:
            self.body.angle = clockwise_degrees_to_anti_clockwise_radian(
                self.internal_ship.target_angle
            )
            self.internal_ship.target_angle = None
            self.body.angular_velocity = 0
        else:
            angular_velocity = (
                self.internal_ship.rotation_engine_power * self.internal_ship.rotation_engine_percent / 100
            )
            angular_velocity = (
                -angular_velocity if angular_diff > 0 else angular_velocity
            )
            self.body.angular_velocity = math.radians(angular_velocity)

    @property
    def sector_coords(self):
        return get_sector_coords(self.body.position)

    def get_sector(self):
        return Sector.get_sector(self.sector_coords)

    def enter_sector(self):
        sector = self.get_sector()
        sector.add_ship(self)
        self.sector = sector

    def leave_sector(self):
        self.sector.remove_ship(self)
        self.sector = None

    @property
    def in_hyperspace(self):
        return self.sector is None

    def tick(self):
        # TODO: Firstly use panels to generate physical phenomenons
        # TODO: Secondly, use the tick of each physical phenomenon
        if self.in_hyperspace:
            self._rotate()
            self._add_engine_force()
        else:
            pass


class Sector:
    sectors_map = {}

    def __init__(self, position: Vec2d):
        self.ships = set()
        self.structures = set()
        self.allegiance = None
        self._position = position
        self.name = "Sector {}".format(position)
        self.state = SectorStateEnum.LOADED
        self.sectors_map[position] = self

    @classmethod
    def get_sector(cls, position: Vec2d):
        sector = cls.sectors_map.get((position.x, position.y), None)
        if not sector:
            sector = cls(position)
        return sector

    @property
    def x(self):
        return self._position.x

    @property
    def y(self):
        return self._position.y

    def add_ship(self, ship: HyperspaceShip):
        self.ships.add(ship)

    def remove_ship(self, ship: HyperspaceShip):
        self.ships.remove(ship)


class SectorStateEnum(str, Enum):
    #  Note: optimization potential here, switching to int enum might reduce the cost of storing a sector.
    LOADED = "loaded"
