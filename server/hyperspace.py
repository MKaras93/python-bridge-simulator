from pygame.time import Clock
import math


class Ship:
    ships = []

    def __init__(self, x: float, y: float, velocity: float, facing: int):
        self.ships.append(self)
        self.x = x
        self.y = y
        self.velocity = velocity
        self._facing = facing

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

    def tick(self):
        self._update_position()
        print(self.x, self.y)


clock = Clock()


def main_loop():
    running = True

    while running:
        for ship in Ship.ships:
            ship.tick()
        clock.tick(2)


main_sheep = Ship(0, 0, 0.01, 45)
