import math

from pymunk import Vec2d


class PygamePymunkImplementationUnitsTransformer:
    """
    Class responsible for translating units between pymunk/pygame and units used in the Game.
    Part of the Game setting.
    """
    @staticmethod
    def to_impl_position(position: Vec2d) -> Vec2d:
        return Vec2d(position[0], -position[1])

    @staticmethod
    def from_impl_position(impl_position: Vec2d) -> Vec2d:
        return Vec2d(impl_position[0], -impl_position[1])

    @staticmethod
    def to_impl_angle(angle_degree: float) -> float:
        degrees = (angle_degree + 270) % 360
        return math.radians(degrees)

    @staticmethod
    def from_impl_angle(impl_angle: float) -> float:
        degrees = math.degrees(impl_angle)
        return (degrees + 90) % 360
