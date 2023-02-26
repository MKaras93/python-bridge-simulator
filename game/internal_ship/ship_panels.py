from __future__ import annotations

import abc
from typing import Optional, Any
from typing import TYPE_CHECKING

from game.errors import (
    NoSuchPanelAttributeException,
    NoSuchPanelException,
)

from game.internal_ship.phenomenons import Hypersphere
from game.internal_ship.enums import PhenomenonState

if TYPE_CHECKING:
    from game.internal_ship.classes import InternalShip


class ShipPanel(abc.ABC):
    panel_type = None

    def __init__(self):
        self.internal_ship: Optional[InternalShip] = None

    def attach_to_ship(self, internal_ship: InternalShip):
        self.internal_ship = internal_ship
        print("Attached panel:", self)

    def _validate_attribute_name(self, attribute_name: str):
        if attribute_name.startswith("_") or not hasattr(self, attribute_name):
            raise NoSuchPanelAttributeException(
                f"Panel {self.panel_type} doesn't have attribute '{attribute_name}'."
            )

    def get_attribute(self, attribute_name: str):
        # if anything aside happens during reading, it should happen here.
        self._validate_attribute_name(attribute_name)
        return getattr(self, attribute_name)

    def set_attribute(self, attribute_name: str, value: Any):
        self._validate_attribute_name(attribute_name)
        setattr(self, attribute_name, value)
        return value

    def call_method(self, method_name, **kwargs):
        self._validate_attribute_name(method_name)  # method is just an attribute - same logic
        # TODO: think of some argument validation - there would be different validation for each method. Pydantic?
        method = getattr(self, method_name)
        return method(**kwargs)

    @property
    def operators(self):
        # if no one has permission, every one has permission.
        return self.internal_ship.panel_permissions.get(self.panel_type, self.internal_ship.bridge_crew)

    def log(self, level: str, message: str):
        self.internal_ship.simulation.game.log(level=level, message=message, panel=self)


class Cockpit(ShipPanel):
    panel_type = "cockpit"

    @property
    def target_angle(self) -> float:
        return self.internal_ship.target_angle

    @target_angle.setter
    def target_angle(self, value: float):
        if value is not None and not self.rotation_drive_percent:
            self.log("warning", "Target angle set but rotation drive is off.")
        self.internal_ship.target_angle = value

    @property
    def hyper_drive_percent(self) -> float:
        return self.internal_ship.engine_percent

    @hyper_drive_percent.setter
    def hyper_drive_percent(self, value: float):
        self.internal_ship.engine_percent = value

    @property
    def rotation_drive_percent(self) -> float:
        return self.internal_ship.rotation_engine_percent

    @rotation_drive_percent.setter
    def rotation_drive_percent(self, value: float):
        self.internal_ship.rotation_engine_percent = value

    @property
    def hyper_drive_timer(self) -> int:
        return self.internal_ship.engine_cut_off_time

    @hyper_drive_timer.setter
    def hyper_drive_timer(self, value: int):
        self.internal_ship.engine_cut_off_time = value

    @property
    def hypersphere_generator_enabled(self) -> bool:
        return self.internal_ship.modules.hypersphere_generator.enabled

    @hypersphere_generator_enabled.setter
    def hypersphere_generator_enabled(self, value: bool):
        self.internal_ship.modules.hypersphere_generator.enabled = value

    def disengage_hyper_drive(self, timer: int = 0):
        # mocked method to test method calls
        print(f"Disengaging hyper drive in {timer}")
        print(f"Hyper drive disengaged!")
        return True


class Configuration(ShipPanel):
    """
    Panel responsible for different settings, such as permissions to different panels.
    """
    panel_type = "configuration"

    @property
    def permissions(self) -> int:
        return self.internal_ship.panel_permissions

    @permissions.setter
    def permissions(self, value: dict):
        self.internal_ship.panel_permissions = value


class ShipPanels:
    def __init__(self):
        self.cockpit: Optional[Cockpit] = None

    def validate_panel_name(self, panel_name: str):
        if panel_name.startswith("_") or not hasattr(self, panel_name):
            raise NoSuchPanelException(f"Panel '{panel_name}' does not exist.")


class HypersphereGenerator:
    module_type = "hypersphere_generator"

    def __init__(self, power: int):
        self.internal_ship: Optional[InternalShip] = None
        self.power = power
        self._enabled = False

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        if self._enabled != value:
            self._enabled = value
            state = "ENABLED" if value else "DISABLED"
            self.internal_ship.panels.cockpit.log("info", f"Hypersphere Generator is now {state}.")

    def attach_to_ship(self, internal_ship: InternalShip):
        self.internal_ship = internal_ship
        self.internal_ship.modules.attached.add(self)
        print("Attached module:", self)

    def tick(self):
        if self.enabled:
            hypersphere = self.internal_ship.hypersphere
            if not hypersphere:
                self.internal_ship.panels.cockpit.log("info", f"Generating new hypersphere with power {self.power}.")
                Hypersphere(self.internal_ship, power=self.power, state=PhenomenonState.PENDING)
            else:
                hypersphere.power_up(1)


class ShipModules:
    attached = set()

    def __init__(self):
        self.hypersphere_generator: Optional[HypersphereGenerator] = None
