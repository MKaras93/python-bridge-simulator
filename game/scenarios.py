from __future__ import annotations

import random

from game.hyperspace import HyperspaceShip
from game.player_ship import PlayerShip
from game.ship_modules import Cockpit

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.loop import Simulation

class BaseScenario:
    PLAYER_SHIP_MODULES = [
            Cockpit(),
        ]

    def __init__(self, game: Simulation):
        self.game: Simulation = game

    def play(self, ct: int):
        if ct == 1:
            self._setup()
        pass

    def _setup(self):
        print(f"Setting up {self.__class__}.")

    def _setup_player_ship(self):
        print("adding player ship")
        starting_coords = (500, 500)
        hyperspace_ship: HyperspaceShip = self.game.space.create_ship(starting_coords)
        hyperspace_ship.engine_percent = 0
        hyperspace_ship.rotation_engine_percent = 0
        self.game.space.ships.append(hyperspace_ship)

        player_ship = PlayerShip(
            game=self.game,
            hyperspace_ship=hyperspace_ship,
        )
        for module in self.PLAYER_SHIP_MODULES:
            player_ship.add_module(module)

        self.game.player_ship = player_ship


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
            print(
                f"setting new target angle to {new_value}. Current angle: {ship.angle}."
            )
            ship.target_angle = new_value

    def _turn_off_engines_during_rotation(self):
        for ship in self.game.space.ships:
            if ship.target_angle is not None:
                ship.engine_percent = 0
            else:
                ship.engine_percent = 10


class PlayerShipTestScenario(BaseScenario):
    def _setup(self):
        super()._setup()
        self._setup_player_ship()

    def play(self, ct: int):
        super().play(ct)
        # print(self.game.player_ship.modules.cockpit.target_angle)
        # self.game.player_ship.modules.cockpit.target_angle = 150
        # print(self.game.player_ship.hyperspace_ship.target_angle)


ACTIVE_SCENARIO = PlayerShipTestScenario
