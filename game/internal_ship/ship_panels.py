from __future__ import annotations

import abc
from typing import Optional, Any
from typing import TYPE_CHECKING

from pymunk import Vec2d

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
        self._validate_attribute_name(
            method_name
        )  # method is just an attribute - same logic
        # TODO: think of some argument validation - there would be different validation for each method. Pydantic?
        method = getattr(self, method_name)
        return method(**kwargs)

    @property
    def operators(self):
        # if no one has permission, every one has permission.
        return self.internal_ship.panel_permissions.get(
            self.panel_type, self.internal_ship.bridge_crew
        )

    def log(self, level: str, message: str):
        self.internal_ship.simulation.game.log(level=level, message=message, panel=self)


class Cockpit(ShipPanel):
    panel_type = "cockpit"

    @property
    def position(self) -> Vec2d:
        if self.internal_ship.sector_ship:
            return self.internal_ship.sector_ship.sector.position
        else:
            return self.internal_ship.hyperspace_ship.position

    @property
    def target_angle(self) -> float:
        return self.internal_ship.target_angle

    @target_angle.setter
    def target_angle(self, value: float):
        self.log("INFO", f"Target angle set to {value} degrees.")
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

    @property
    def status(self) -> None:
        return None

    @property
    def autopilot_enabled(self) -> bool:
        return self.internal_ship.modules.autopilot.enabled

    @autopilot_enabled.setter
    def autopilot_enabled(self, value: bool):
        self.internal_ship.modules.autopilot.enabled = value

    @property
    def autopilot_target_destination(self) -> Optional[Vec2d]:
        return self.internal_ship.modules.autopilot.target_position

    @autopilot_target_destination.setter
    def autopilot_target_destination(self, value: Vec2d):
        self.log("INFO", f"Autopilot set to {value}")
        self.internal_ship.modules.autopilot.target_position = value


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


class ShipModule(abc.ABC):
    module_type: str = None
    logging_panel_type: str = None

    def __init__(self):
        self.internal_ship: Optional[InternalShip] = None
        self._logging_panel: Optional[ShipPanel] = None

    def attach_to_ship(self, internal_ship: InternalShip):
        self.internal_ship = internal_ship
        self.internal_ship.modules.attached.add(self)
        self._logging_panel = getattr(self.internal_ship.panels, self.logging_panel_type)
        print("Attached module:", self)

    def tick(self):
        pass

    def log(self, level: str, message: str) -> None:
        self._logging_panel.log(level, message)


class HypersphereGenerator(ShipModule):
    module_type = "hypersphere_generator"
    logging_panel_type = "cockpit"

    def __init__(self, power: int):
        super().__init__()
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
            self.log(
                "info", f"Hypersphere Generator is now {state}."
            )

    def tick(self):
        super().tick()
        if self.enabled:
            hypersphere = self.internal_ship.hypersphere
            if not hypersphere:
                self.log(
                    "info", f"Generating new hypersphere with power {self.power}."
                )
                Hypersphere(
                    self.internal_ship, power=self.power, state=PhenomenonState.PENDING
                )
            else:
                hypersphere.power_up(1)


class RotationDrive(ShipModule):
    module_type = "rotation_drive"
    logging_panel_type = "cockpit"

    def __init__(self, tick_rotation: float):
        super().__init__()
        self.tick_rotation = tick_rotation

    def tick(self):
        super().tick()
        if self.internal_ship.hyperspace_ship:
            self._rotate_ship()

    def _rotate_ship(self):
        target_angle = self.internal_ship.panels.cockpit.target_angle
        if target_angle is None or target_angle == self.internal_ship.hyperspace_ship.angle:
            return

        rotation_value = self._get_rotation_value(
            current_angle=self.internal_ship.hyperspace_ship.angle,
            target_angle=target_angle,
        )
        rotation_sign = -1 if rotation_value < 0 else 1

        if abs(rotation_value) > self.tick_rotation:
            rotation_value = self.tick_rotation * rotation_sign

        self.internal_ship.hyperspace_ship.angle += rotation_value
        if self.internal_ship.hyperspace_ship.angle == target_angle:
            self.log("INFO", "Target angle locked.")

    @staticmethod
    def _get_rotation_value(current_angle: float, target_angle: float):
        angle_diff = target_angle - current_angle
        if abs(angle_diff) > 180:
            sign = -1 if angle_diff > 0 else 1
            angle_diff = angle_diff + sign * 360

        return angle_diff


class Autopilot(ShipModule):
    module_type = "autopilot"
    logging_panel_type = "cockpit"

    def __init__(self):
        super().__init__()
        self.target_position: Optional[Vec2d] = None
        self.enabled = False
        self._previous_distance = None

    def tick(self):
        super().tick()
        if (
            not self.internal_ship.hyperspace_ship
            or not self.enabled
            or self.target_position is None
        ):
            return

        distance_to_target = self._get_distance_to_target()
        if distance_to_target <= 0.5:
            self.log("INFO", "Destination in range.")
            self._stop_ship()
            self.target_position = None
            return

        if (
            self._previous_distance is not None
            and distance_to_target > self._previous_distance
        ):
            self.log("WARNING", "Wrong direction! Moving away from the destination!")
            self._stop_ship()
            return

        self._previous_distance = distance_to_target

    def _get_distance_to_target(self) -> float:
        return self.internal_ship.hyperspace_ship.position.get_distance(
            self.target_position
        )

    def _stop_ship(self):
        self.log("INFO", "Stopping hyper drive. Disengaging Autopilot.")
        self.internal_ship.panels.cockpit.hyper_drive_percent = 0
        self.enabled = False
        self._previous_distance = None


class ShipModules:
    attached = set()

    def __init__(self):
        self.hypersphere_generator: Optional[HypersphereGenerator] = None
        self.rotation_drive: Optional[RotationDrive] = None
        self.autopilot: Optional[Autopilot] = None
