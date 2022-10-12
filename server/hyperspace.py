import datetime
from typing import Tuple, List

import math
import pymunk
from pymunk import Vec2d

from server.utils import clockwise_degrees_to_anti_clockwise_radian, anticlockwise_radian_to_clockwise_degrees


class HyperSpace(pymunk.Space):
    def __init__(self, threaded=False):
        super().__init__(threaded=threaded)
        self.ships = []

    def create_ship(self, position: Tuple[float, float], angle_degree: float = 0):
        ship = HyperspaceShip()
        ship.body.position = position
        ship.body.angle = math.radians(angle_degree)
        self.add(ship.body)
        self.ships.append(ship)
        return ship

    def tick(self):
        for ship in self.ships:
            ship.tick()


class HyperspaceShip:
    def __init__(self):
        self.body = pymunk.Body(body_type=pymunk.Body.DYNAMIC, mass=1, moment=1)
        self.engine_percent: int = 0
        self.engine_power = 100
        self.engine_cut_off_time = None
        self.rotation_engine_power = 100
        self.rotation_engine_percent: int = 0
        self.target_angle = None

    @property
    def angle(self) -> float:
        return anticlockwise_radian_to_clockwise_degrees(self.body.angle)

    @angle.setter
    def angle(self, value: int):
        self.body.angle = clockwise_degrees_to_anti_clockwise_radian(value)

    def _cut_off_engine(self):
        self.engine_percent = 0
        self.engine_cut_off_time = None

    def _add_engine_force(self):
        if self.engine_percent != 0:
            speed = self.engine_percent/100*self.engine_power
            force_vector = Vec2d(speed, 0)
            self.body.apply_force_at_local_point(force_vector)

        if self.engine_cut_off_time is not None:
            now = datetime.datetime.now()
            if now >= self.engine_cut_off_time:
                self._cut_off_engine()

    def _rotate(self):
        if self.target_angle is None:
            return

        angular_diff = self.target_angle - self.angle
        if abs(angular_diff) <= 1:
            self.body.angle = clockwise_degrees_to_anti_clockwise_radian(self.target_angle)
            self.target_angle = None
            self.body.angular_velocity = 0
        else:
            angular_velocity = self.rotation_engine_power * self.rotation_engine_percent/100
            angular_velocity = -angular_velocity if angular_diff > 0 else angular_velocity
            self.body.angular_velocity = math.radians(angular_velocity)

    def tick(self):
        # print(f"Ticking {self}")
        self._rotate()
        self._add_engine_force()
