import math


def clockwise_degrees_to_anti_clockwise_radian(degrees: float):
    inverted_degrees = 450 - (degrees % 360)
    return math.radians(inverted_degrees)


def anticlockwise_radian_to_clockwise_degrees(radians: float):
    inverted_degrees = math.degrees(radians)
    return (450 - inverted_degrees) % 360