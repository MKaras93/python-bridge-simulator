from pygame.time import Clock
import math
import matplotlib.pyplot as plt


class HyperspaceCoords:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


class HyperspaceObject(HyperspaceCoords):
    def __init__(self, x: float, y: float):
        super().__init__(x, y)


class MovingHyperspaceObject(HyperspaceObject):
    def __init__(self, x: float, y: float, velocity: float, facing: int):
        super().__init__(x, y)
        self.velocity = velocity
        self.facing = facing

    @property
    def facing(self):
        return self._facing

    @facing.setter
    def facing(self, value):
        self._facing = value % 360

    def _update_position(self):
        f = math.radians(self.facing)
        self.x = round(self.x + math.sin(f) * self.velocity, 2)
        self.y = round(self.y + math.cos(f) * self.velocity, 2)

    def tick(self, debug: bool = False):
        self._update_position()
        print(self.x, self.y)
        if debug:
            plt.scatter(self.x, self.y)


class HyperspaceShip(MovingHyperspaceObject):
    ships = []

    def __init__(self, x: float, y: float, velocity: float, facing: int):
        super().__init__(x, y, velocity, facing)
        self.ships.append(self)


class Sector(HyperspaceObject):
    def __init__(self, x: float, y: float):
        super().__init__(x, y)


def tick(clock, debug: bool = False):
    for ship in HyperspaceShip.ships:
        ship.tick(debug=debug)
    clock.tick(2)


def main_loop(ticks=None, clock=None, debug: bool = False):
    if clock is None:
        clock = Clock()

    running = True

    if ticks is None:
        while running:
            tick(clock, debug=debug)
        return

    for tick_num in range(0, ticks):
        tick(clock, debug=debug)
    return


main_ship = HyperspaceShip(0, 0, 0.01, 45)
