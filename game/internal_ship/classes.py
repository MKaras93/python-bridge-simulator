from __future__ import annotations

import typing

from pymunk import Vec2d

from game.hyperspace.classes import HyperspaceShip
from game.internal_ship.ship_panels import ShipPanels, ShipModules
from game.sectors.classes import SectorShip, Sector

if typing.TYPE_CHECKING:
    from game.core import Simulation
    from game.hyperspace.classes import Hyperspace
    from game.internal_ship.ship_panels import ShipPanel


class InternalShip:
    """
    Represents ship internals - its modules, integrity, settings, commodities, crew etc. Everything that should be
    preserved in a ship between sectors and hyperspace.
    """

    def __init__(self, simulation: Simulation):
        self.simulation: Simulation = simulation
        self.simulation.internal_ships.add(self)
        self.space: Hyperspace = simulation.space
        self.hyperspace_ship: typing.Optional[HyperspaceShip] = None
        self.sector_ship: typing.Optional[SectorShip] = None
        self.panels: ShipPanels = ShipPanels()
        self.modules: ShipModules = ShipModules()
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

        self.hypersphere = None

    def add_panel(self, panel: ShipPanel):
        setattr(self.panels, panel.panel_type, panel)
        panel.attach_to_ship(self)

    def add_module(self, module):
        setattr(self.modules, module.module_type, module)
        module.attach_to_ship(self)

    def create_hyperspace_ship(self, position: Vec2d) -> HyperspaceShip:
        print("Entering hyperspace at ", position)
        self.hyperspace_ship = HyperspaceShip(self, position)
        return self.hyperspace_ship

    def create_sector_ship(self, position: Vec2d) -> SectorShip:
        print("Leaving hyperspace at ", position)
        sector = Sector.get_sector(position)
        self.sector_ship = SectorShip(self, sector)
        return self.sector_ship

    def tick(self):
        in_hyperspace = True if self.hypersphere else False

        if in_hyperspace:
            if self.hyperspace_ship is None:
                self.create_hyperspace_ship(self.sector_ship.sector.position)
                self.sector_ship.destroy()
        else:
            if self.sector_ship is None:
                self.create_sector_ship(self.hyperspace_ship.position)
                self.hyperspace_ship.destroy()

        for module in self.modules.attached:
            module.tick()

        if self.hyperspace_ship:
            self.hyperspace_ship.tick()
        elif self.sector_ship:
            self.sector_ship.tick()
