import random

from pymunk import Vec2d

from game.hyperspace import HyperspaceShip

class BaseScenario:
    def __init__(self, game: "Game"):
        self.game = game

    def play(self, ct: int):
        if ct == 1:
            self._setup()

    def _setup(self):
        print(f"Setting up {self.__class__}.")


class RandomShipsScenario(BaseScenario):
    def _add_random_ship(self):
        print("adding random ship")
        new_ship_coord = random.randint(0, 500), random.randint(0, 500)
        new_ship: HyperspaceShip = self.game.space.create_ship(new_ship_coord)
        new_ship.engine_percent = 10
        new_ship.rotation_engine_percent = 10

        self.game.space.ships.append(new_ship)

    def _setup(self):
        super()._setup()
        for i in range(0, 4):
            self._add_random_ship()

        self._set_random_target_angle_for_ships()

    def play(self, ct: int):
        super().play(ct)

        self._turn_off_engines_during_rotation()

        if ct % 200 == 0:
            self._set_random_target_angle_for_ships()

    def _set_random_target_angle_for_ships(self):
        for ship in self.game.space.ships:
            new_value = random.randint(0, 360)
            print(f"setting new target angle to {new_value}. Current angle: {ship.angle}.")
            ship.target_angle = new_value

    def _turn_off_engines_during_rotation(self):
        for ship in self.game.space.ships:
            if ship.target_angle is not None:
                ship.engine_percent = 0
            else:
                ship.engine_percent = 10


def _fly_to_point(ship: HyperspaceShip, target_x, target_y):
    ship.rotation_engine_percent = 0
    ship.engine_percent = 0
    angle = ship.body.position.get_angle_degrees_between(Vec2d(target_x, target_y))
    print("angle:", angle)
    ship.target_angle = ship.angle - angle
    if ship.target_angle:
        ship.rotation_engine_percent = 50

    if ship.angle - ship.target_angle < 5:
        ship.rotation_engine_percent = 0
        distance = ship.body.position.get_distance((target_x, target_y))
        print("distance to target:", distance)
        ship.engine_percent = distance
        if distance <= 10:
            print("Target in sight!")


ACTIVE_SCENARIO = RandomShipsScenario
