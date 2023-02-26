import math

import pymunk
from pymunk import Vec2d


def clockwise_degrees_to_anti_clockwise_radian(degrees: float) -> float:
    inverted_degrees = 450 - (degrees % 360)
    return math.radians(inverted_degrees)


def anticlockwise_radian_to_clockwise_degrees(radians: float) -> float:
    inverted_degrees = math.degrees(radians)
    return (450 - inverted_degrees) % 360


def create_circle_for_body(space: "Hyperspace", body: pymunk.Body, radius=10):
    circle = pymunk.Circle(body, radius=radius)
    space.add(circle)


def get_sector_coords(position):
    SECTOR_SIZE = 10

    def _get_sector_coord(coord: float) -> int:
        return math.ceil(coord / SECTOR_SIZE)

    return Vec2d(_get_sector_coord(position.x), _get_sector_coord(position.y))


def get_course(from_point: Vec2d, to_point: Vec2d) -> float:
    result = (to_point - from_point).get_angle_degrees_between(Vec2d(0, 1))
    result = result + 360 if result < 0 else result
    return result
