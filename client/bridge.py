from __future__ import annotations

from client.http_client.api_client import APIClient, BaseClient

CLIENT_CLASS = APIClient


class BasePanel:
    def __init__(self, ship: MotherShip, client):
        self.ship: MotherShip = ship
        self._client: BaseClient = client


class Cockpit(BasePanel):
    panel_type = "cockpit"

    @property
    def hypersphere_generator_enabled(self) -> bool:
        return self._client.get_attribute(self.panel_type, "hypersphere_generator_enabled")

    @hypersphere_generator_enabled.setter
    def hypersphere_generator_enabled(self, value: bool):
        self._client.set_attribute(self.panel_type, "hypersphere_generator_enabled", value)

    @property
    def target_angle(self) -> float:
        return self._client.get_attribute(self.panel_type, "target_angle")

    @target_angle.setter
    def target_angle(self, value: float):
        self._client.set_attribute(self.panel_type, "target_angle", value)

    @property
    def hyper_drive_percent(self) -> float:
        return self._client.get_attribute(self.panel_type, "hyper_drive_percent")

    @hyper_drive_percent.setter
    def hyper_drive_percent(self, value: float):
        self._client.set_attribute(self.panel_type, "hyper_drive_percent", value)

    @property
    def rotation_drive_percent(self) -> float:
        return self._client.get_attribute(self.panel_type, "rotation_drive_percent")

    @rotation_drive_percent.setter
    def rotation_drive_percent(self, value: float):
        self._client.set_attribute(self.panel_type, "rotation_drive_percent", value)

    @property
    def hyper_drive_timer(self) -> float:
        return self._client.get_attribute(self.panel_type, "hyper_drive_timer")

    @hyper_drive_timer.setter
    def hyper_drive_timer(self, value: float):
        self._client.set_attribute(self.panel_type, "hyper_drive_timer", value)

    def disengage_hyper_drive(self, timer: int = 0):
        return self._client.call_method(self.panel_type, "disengage_hyper_drive", timer=timer)


class MotherShip:
    def __init__(self):
        self._client = CLIENT_CLASS(self)
        self.cockpit: Cockpit = self._add_panel(Cockpit)

    def _add_panel(self, panel_class: type):
        panel = panel_class(self, client=self._client)
        return panel

    def log(self, panel: str, level: str, message: str, user: str, timestamp: str):
        print(f"[{timestamp}][{level}][{panel.upper()}]: {message}")


MS = MotherShip()
