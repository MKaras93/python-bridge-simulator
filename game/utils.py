import math
from decimal import Decimal, ROUND_HALF_UP

import pymunk
from pymunk import Vec2d


def create_circle_for_body(space: "Hyperspace", body: pymunk.Body, radius=10):
    circle = pymunk.Circle(body, radius=radius)
    space.add(circle)


def get_sector_coords(position):
    SECTOR_SIZE = 1

    def _get_sector_coord(coord: float) -> int:
        # 1.2 -> 1,
        # 0.5 -> 1
        # 0.1 -> 0
        scaled_coord = Decimal(coord/SECTOR_SIZE)
        return int(scaled_coord.to_integral_value(rounding=ROUND_HALF_UP))

    return Vec2d(_get_sector_coord(position[0]), _get_sector_coord(position[1]))


def get_course(from_point: Vec2d, to_point: Vec2d) -> float:
    result = (to_point - from_point).get_angle_degrees_between(Vec2d(0, 1))
    result = result + 360 if result < 0 else result
    return result
