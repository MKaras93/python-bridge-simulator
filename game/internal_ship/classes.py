from __future__ import annotations

import typing

from pymunk import Vec2d

from game.hyperspace.classes import HyperspaceShip
from game.internal_ship.ship_panels import ShipPanels, ShipPanel

if typing.TYPE_CHECKING:
    from game.core import Simulation
    from game.hyperspace.classes import Hyperspace


class InternalShip:
    """
    Represents ship internals - its modules, integrity, settings, commodities, crew etc. Everything that should be
    preserved in a ship between sectors and hyperspace.
    """

    def __init__(self, simulation: Simulation):
        self.simulation: Simulation = simulation
        self.space: Hyperspace = simulation.space
        self.hyperspace_ship: typing.Optional[HyperspaceShip] = None
        self.panels: ShipPanels = ShipPanels()
        self.panel_names = set()
        self.bridge_crew = [
            # TODO: placeholder for usernames of the bridge crew members
            "test",
        ]
        self.panel_permissions = {}

        self.engine_percent: int = 0
        self.engine_power = 100
        self.engine_cut_off_time = None
        self.rotation_engine_power = 100
        self.rotation_engine_percent: int = 10
        self.target_angle = None

    def add_panel(self, panel: ShipPanel):
        setattr(self.panels, panel.panel_type, panel)
        self.panel_names.add(panel.panel_type)
        panel.attach_to_ship(self)

    def create_hyperspace_ship(self, position: Vec2d) -> HyperspaceShip:
        self.hyperspace_ship = HyperspaceShip(self, position)
        return self.hyperspace_ship
