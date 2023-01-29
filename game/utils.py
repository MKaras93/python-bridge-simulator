import math
import random

import pymunk


def clockwise_degrees_to_anti_clockwise_radian(degrees: float) -> float:
    inverted_degrees = 450 - (degrees % 360)
    return math.radians(inverted_degrees)


def anticlockwise_radian_to_clockwise_degrees(radians: float) -> float:
    inverted_degrees = math.degrees(radians)
    return (450 - inverted_degrees) % 360


def create_circle_for_body(space: "HyperSpace", body: pymunk.Body, radius=10):
    circle = pymunk.Circle(body, radius=radius)
    space.add(circle)


def get_ship(space: "HyperSpace"):
    ship = space.create_ship((random.randint(0, 500), random.randint(0, 500)), 0)
    ship.engine_power = 500
    ship.engine_percent = 10
    create_circle_for_body(space, ship.body)
    ship.rotation_engine_power = 90
    ship.rotation_engine_percent = 50
    ship.angle = 0
    ship.target_angle = 160
    return ship


def get_sector_coord(coord: float) -> int:
    SECTOR_SIZE = 10
    return math.ceil(coord/SECTOR_SIZE)


def get_sector(position):
    return (get_sector_coord(position.x), get_sector_coord(position.y))
