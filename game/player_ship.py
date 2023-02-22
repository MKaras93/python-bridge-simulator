from __future__ import annotations
from typing import TYPE_CHECKING

from game.ship_panels import ShipPanels

if TYPE_CHECKING:
    from game.loop import Simulation
    from game.hyperspace import HyperspaceShip, HyperSpace
    from game.ship_panels import ShipPanel


class PlayerShip:
    """
    Layer between server and object representing ship (in any of the spaces).

    Everything the server (so the players) do has to come through this object.
    Differences between normal npc ship and players ship are implemented here.
    """
    def __init__(self, simulation: Simulation, hyperspace_ship: HyperspaceShip):
        self.simulation: Simulation = simulation
        self.space: HyperSpace = simulation.space
        self.hyperspace_ship: HyperspaceShip = hyperspace_ship
        self.panels: ShipPanels = ShipPanels()
        self.panel_names = set()
        self.bridge_crew = [
            # TODO: placeholder for usernames of the bridge crew members
            "test",
        ]
        self.panel_permissions = {}

    def add_panel(self, panel: ShipPanel):
        setattr(self.panels, panel.panel_type, panel)
        self.panel_names.add(panel.panel_type)
        panel.attach_to_ship(self)
