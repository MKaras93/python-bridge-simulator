from __future__ import annotations

from typing import Optional
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.hyperspace import HyperspaceShip
    from game.player_ship import PlayerShip


class ShipModule:
    module_type = None

    def __init__(self):
        self.player_ship: Optional[PlayerShip] = None
        self.hyperspace_ship: Optional[HyperspaceShip] = None

    def attach_to_ship(self, player_ship: PlayerShip):
        self.player_ship = player_ship
        self.hyperspace_ship = self.player_ship.hyperspace_ship
        print("Attached module:", self)


class Cockpit(ShipModule):
    module_type = "cockpit"

    def __init__(self):
        super().__init__()

    @property
    def target_angle(self) -> float:
        return self.player_ship.hyperspace_ship.target_angle

    @target_angle.setter
    def target_angle(self, value: float):
        self.hyperspace_ship.target_angle = value

    @property
    def hyper_drive_percent(self) -> float:
        return self.hyperspace_ship.engine_percent

    @hyper_drive_percent.setter
    def hyper_drive_percent(self, value: float):
        self.hyperspace_ship.engine_percent = value

    @property
    def rotation_drive_percent(self) -> float:
        return self.hyperspace_ship.rotation_engine_percent

    @rotation_drive_percent.setter
    def rotation_drive_percent(self, value: float):
        self.hyperspace_ship.rotation_engine_percent = value

    @property
    def hyper_drive_timer(self) -> int:
        return self.hyperspace_ship.engine_cut_off_time

    @hyper_drive_timer.setter
    def hyper_drive_timer(self, value: int):
        self.hyperspace_ship.engine_cut_off_time = value


class ShipSubmodule:
    pass


class ShipModules:
    def __init__(self):
        self.cockpit = Optional[Cockpit]