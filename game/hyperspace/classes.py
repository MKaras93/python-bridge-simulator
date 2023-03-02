from __future__ import annotations

import datetime
import typing

import pymunk

from pymunk import Vec2d

from game.sectors.classes import Sector
from game.utils import (
    get_sector_coords,
)


if typing.TYPE_CHECKING:
    from typing import List, Optional
    from game.internal_ship.classes import InternalShip
    from game.core import Simulation


class Hyperspace(pymunk.Space):
    def __init__(self, simulation: Simulation, threaded=False):
        super().__init__(threaded=threaded)
        self.simulation = simulation
        self.ships: List[HyperspaceShip] = []


class HyperspaceShip:
    def __init__(self, internal_ship: InternalShip, position: Vec2d):
        self.internal_ship: InternalShip = internal_ship
        self.space: Hyperspace = internal_ship.space

        self._body = pymunk.Body(body_type=pymunk.Body.DYNAMIC, mass=1, moment=1)
        self._circle = pymunk.Circle(self._body, radius=10)
        self.space.add(self._body)
        self.space.add(self._circle)
        self.space.ships.append(self)
        self.position = position

        self.sector: Optional[Sector] = None

    @property
    def position(self) -> Vec2d:
        return self.space.simulation.transformer.from_impl_position(self._body.position)

    @position.setter
    def position(self, value: Vec2d):
        self._body.position = self.space.simulation.transformer.to_impl_position(value)

    def destroy(self):
        self.internal_ship.hyperspace_ship = None
        self.internal_ship = None
        self.space.ships.remove(self)
        self.space.remove(self._body, self._circle)
        print("{} destroyed.".format(self))

    @property
    def angle(self) -> float:
        return self.space.simulation.transformer.from_impl_angle(self._body.angle)

    @angle.setter
    def angle(self, value: float):
        self._body.angle = self.space.simulation.transformer.to_impl_angle(value)

    def _cut_off_engine(self):
        # TODO: move to modules or panels behaviour
        self.internal_ship.engine_percent = 0
        self.internal_ship.engine_cut_off_time = None

    def _add_engine_force(self):
        if self.internal_ship.engine_percent == 0:
            return
        else:
            speed = (
                self.internal_ship.engine_percent
                / 100
                * self.internal_ship.engine_power
            )
            force_vector = Vec2d(speed, 0)
            self._body.apply_force_at_local_point(force_vector)

        if self.internal_ship.engine_cut_off_time is not None:
            now = datetime.datetime.now()
            if now >= self.internal_ship.engine_cut_off_time:
                self._cut_off_engine()

    @property
    def sector_coords(self):
        return get_sector_coords(self.position)

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
            self._add_engine_force()
        else:
            pass
