from __future__ import annotations

import abc
from typing import Optional, Any
from typing import TYPE_CHECKING

from game.errors import (
    NoSuchModuleAttributeException,
    NoSuchModuleException,
)

if TYPE_CHECKING:
    from game.hyperspace import HyperspaceShip
    from game.player_ship import PlayerShip


class ShipModule(abc.ABC):
    module_type = None

    def __init__(self):
        self.player_ship: Optional[PlayerShip] = None
        self.hyperspace_ship: Optional[HyperspaceShip] = None

    def attach_to_ship(self, player_ship: PlayerShip):
        self.player_ship = player_ship
        self.hyperspace_ship = self.player_ship.hyperspace_ship
        print("Attached module:", self)

    def _validate_attribute_name(self, attribute_name: str):
        if attribute_name.startswith("_") or not hasattr(self, attribute_name):
            raise NoSuchModuleAttributeException(
                f"Module {self.module_type} doesn't have attribute '{attribute_name}'."
            )

    def read_attr(self, attribute_name: str):
        # if anything aside happens during reading, it should happen here.
        self._validate_attribute_name(attribute_name)
        return getattr(self, attribute_name)

    def write_attr(self, attribute_name: str, value: Any):
        self._validate_attribute_name(attribute_name)
        setattr(self, attribute_name, value)
        return value


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

    def validate_module_name(self, module_name: str):
        if module_name.startswith("_") or not hasattr(self, module_name):
            raise NoSuchModuleException(f"Module '{module_name}' does not exist.")
