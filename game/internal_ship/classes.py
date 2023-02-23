from __future__ import annotations

import typing
from enum import Enum

from pymunk import Vec2d

from game.hyperspace.classes import HyperspaceShip
from game.internal_ship.ship_panels import ShipPanels, ShipPanel
from game.sectors.classes import SectorShip, Sector

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
        self.simulation.internal_ships.add(self)
        self.space: Hyperspace = simulation.space
        self.hyperspace_ship: typing.Optional[HyperspaceShip] = None
        self.sector_ship: typing.Optional[SectorShip] = None
        self.panels: ShipPanels = ShipPanels()
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


class PhenomenonState(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    DELETED = "deleted"


class Hypersphere:
    def __init__(self, ship: InternalShip, power: int, state: PhenomenonState.PENDING):
        print("New Hypersphere created")
        self.ship: InternalShip = ship
        self.ship.hypersphere = self
        self.power: int = power
        self.state: PhenomenonState = state
        self.simulation = self.ship.simulation
        self.simulation.phenomenons.add(self)

    def tick(self):
        if self.state == PhenomenonState.PENDING:
            self.activate()

        self.power -= 1
        print(f"Hypersphere has {self.power} power left")
        if self.power <= 0:
            self.destroy()

    def power_up(self, value: int):
        self.power += value

    def activate(self):
        print("Activating pending hypersphere")
        self.state = PhenomenonState.ACTIVE

    def destroy(self):
        self.ship.hypersphere = None
        self.ship = None
        self.state = PhenomenonState.DELETED
