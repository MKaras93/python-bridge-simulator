from __future__ import annotations

import random

from typing import TYPE_CHECKING

from game.internal_ship.enums import PhenomenonState
from game.internal_ship.phenomenons import Hypersphere

if TYPE_CHECKING:
    from game.core import Simulation
    from game.hyperspace.classes import HyperspaceShip


class BaseScenario:
    from game.internal_ship.ship_panels import Cockpit, HypersphereGenerator

    PLAYER_SHIP_PANELS = [
        Cockpit(),
    ]
    PLAYER_SHIP_MODULES = [
        HypersphereGenerator(power=5),
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
        from game.internal_ship.classes import InternalShip
        print("adding player ship")
        print("setting up internal ship for player ship")
        player_ship = InternalShip(
            simulation=self.game,
        )
        for panel in self.PLAYER_SHIP_PANELS:
            player_ship.add_panel(panel)

        for module in self.PLAYER_SHIP_MODULES:
            player_ship.add_module(module)

        player_ship.engine_percent = 0
        player_ship.rotation_engine_percent = 0
        player_ship.modules.hypersphere_generator.enabled = False

        print("setting up hyperspace ship for player ship")
        starting_position = (500, 500)
        player_ship.create_hyperspace_ship(starting_position)
        # self.game.space.ships.append(hyperspace_ship)
        # internal_ship.hyperspace_ship = hyperspace_ship

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
        self.game.player_ship.target_angle = 50

    def play(self, ct: int):
        super().play(ct)
        # if ct % 100 == 0:
        #     self.game.internal_ship.panels.cockpit.log("error", "Incomming transmission received!")
        # print(self.game.internal_ship.panels.cockpit.target_angle)
        # self.game.internal_ship.panels.cockpit.target_angle = 150
        # print(self.game.internal_ship.hyperspace_ship.target_angle)


class HypersphereTestScenario(BaseScenario):
    def _setup(self):
        super()._setup()
        self._setup_player_ship()
        self.game.player_ship.target_angle = 50
        self.game.player_ship.modules.hypersphere_generator.enabled = True
        self.game.player_ship.hypersphere = Hypersphere(self.game.player_ship, 3, PhenomenonState.ACTIVE)

    def play(self, ct: int):
        super().play(ct)
        # if ct % 100 == 0:
        #     Hypersphere(self.game.player_ship, 10, PhenomenonState.ACTIVE)
        # print(self.game.internal_ship.panels.cockpit.target_angle)
        # self.game.internal_ship.panels.cockpit.target_angle = 150
        # print(self.game.internal_ship.hyperspace_ship.target_angle)


ACTIVE_SCENARIO = HypersphereTestScenario
