from __future__ import annotations

import random

from typing import TYPE_CHECKING

from pymunk import Vec2d

from game.internal_ship.enums import PhenomenonState
from game.internal_ship.phenomenons import Hypersphere
from game.internal_ship.ship_panels import Autopilot
from game.utils import get_course, get_sector_coords

if TYPE_CHECKING:
    from game.core import Simulation
    from game.hyperspace.classes import HyperspaceShip


class BaseScenario:
    from game.internal_ship.ship_panels import (
        Cockpit,
        HypersphereGenerator,
        RotationDrive,
    )

    PLAYER_SHIP_PANELS = [
        Cockpit(),
    ]
    PLAYER_SHIP_MODULES = [
        HypersphereGenerator(power=5),
        RotationDrive(5),
        Autopilot(),
    ]

    def __init__(self, simulation: Simulation):
        self.simulation: Simulation = simulation

    def play(self, ct: int):
        if ct == 1:
            self._setup()
        pass

    def _setup(self):
        print(f"Setting up {self.__class__}.")

    def _setup_player_ship(self, coords=(500, 500), in_hyperspace=True):
        from game.internal_ship.classes import InternalShip

        print("adding player ship")
        print("setting up internal ship for player ship")
        player_ship = InternalShip(
            simulation=self.simulation,
        )
        for panel in self.PLAYER_SHIP_PANELS:
            player_ship.add_panel(panel)

        for module in self.PLAYER_SHIP_MODULES:
            player_ship.add_module(module)

        player_ship.engine_percent = 0
        player_ship.rotation_engine_percent = 0
        player_ship.modules.hypersphere_generator.enabled = False

        if in_hyperspace:
            print("setting up hyperspace ship for player ship")
            player_ship.create_hyperspace_ship(coords)
            player_ship.modules.hypersphere_generator.enabled = True
            player_ship.hypersphere = Hypersphere(
                player_ship, 2, PhenomenonState.ACTIVE
            )
        else:
            print("setting up sector ship for player ship")
            player_ship.create_sector_ship(coords)
        # self.game.space.ships.append(hyperspace_ship)
        # internal_ship.hyperspace_ship = hyperspace_ship

        self.simulation.player_ship = player_ship


class RandomShipsScenario(BaseScenario):
    def _add_random_ship(self):
        print("adding random ship")
        new_ship_coord = random.randint(0, 500), random.randint(0, 500)
        new_ship: HyperspaceShip = self.simulation.space.create_ship(new_ship_coord)
        new_ship.engine_percent = 10
        new_ship.rotation_engine_percent = 10

        self.simulation.space.ships.append(new_ship)

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
        for ship in self.simulation.space.ships:
            new_value = random.randint(0, 360)
            print(
                f"setting new target angle to {new_value}. Current angle: {ship.angle}."
            )
            ship.target_angle = new_value

    def _turn_off_engines_during_rotation(self):
        for ship in self.simulation.space.ships:
            if ship.target_angle is not None:
                ship.engine_percent = 0
            else:
                ship.engine_percent = 10


class PlayerShipTestScenario(BaseScenario):
    def _setup(self):
        super()._setup()
        self._setup_player_ship()
        self.simulation.player_ship.target_angle = 50

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
        self.simulation.player_ship.target_angle = 50
        self.simulation.player_ship.modules.hypersphere_generator.enabled = True
        self.simulation.player_ship.hypersphere = Hypersphere(
            self.simulation.player_ship, 3, PhenomenonState.ACTIVE
        )

    def play(self, ct: int):
        super().play(ct)
        # if ct % 100 == 0:
        #     Hypersphere(self.game.player_ship, 10, PhenomenonState.ACTIVE)
        # print(self.game.internal_ship.panels.cockpit.target_angle)
        # self.game.internal_ship.panels.cockpit.target_angle = 150
        # print(self.game.internal_ship.hyperspace_ship.target_angle)


class SectorToSectorTestScenario(BaseScenario):
    def _setup(self):
        super()._setup()
        starting_coords = Vec2d(random.randint(300, 500), random.randint(300, 500))
        starting_coords = Vec2d(300, -300)
        self.target_coords = Vec2d(305, -305)
        # self.target_coords = Vec2d(400, -400)
        self._setup_player_ship(starting_coords, in_hyperspace=False)
        self.simulation.player_ship.panels.cockpit.log(
            "INFO", f"starting_coords: {starting_coords}"
        )
        self.simulation.player_ship.panels.cockpit.log(
            "INFO", f"target_coords: {self.target_coords}"
        )

    def play(self, ct: int):
        super().play(ct)
        sector_ship = self.simulation.player_ship.sector_ship
        if sector_ship and sector_ship.sector.position == self.target_coords:
            print("YOU HAVE WON")
            self.simulation.player_ship.panels.cockpit.log("IMPORTANT", "YOU HAVE WON!")

        # complete scenario:
        cockpit = self.simulation.player_ship.panels.cockpit
        if ct == 5:
            cockpit.hypersphere_generator_enabled = True
        if ct == 15:
            cockpit.target_angle = get_course(cockpit.position, self.target_coords)
            cockpit.autopilot_target_destination = self.target_coords
            cockpit.autopilot_enabled = True
        if ct == 25:
            cockpit.hyper_drive_percent = 1
        if get_sector_coords(cockpit.position) == self.target_coords:
            cockpit.hypersphere_generator_enabled = False

        # if ct == 5:
        #     self.game.player_ship.panels.cockpit.hypersphere_generator_enabled = True
        #
        # if ct % 100 == 0:
        #     self.game.player_ship.panels.cockpit.target_angle = (
        #         self.game.player_ship.hyperspace_ship.angle + 15
        #     )

        # Hypersphere(self.game.player_ship, 10, PhenomenonState.ACTIVE)
        # print(self.game.internal_ship.panels.cockpit.target_angle)
        # self.game.internal_ship.panels.cockpit.target_angle = 150
        # print(self.game.internal_ship.hyperspace_ship.target_angle)


ACTIVE_SCENARIO = SectorToSectorTestScenario
