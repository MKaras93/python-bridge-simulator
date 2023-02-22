from __future__ import annotations
from typing import TYPE_CHECKING

from game.ship_panels import ShipModules

if TYPE_CHECKING:
    from game.loop import Simulation
    from game.hyperspace import HyperspaceShip, HyperSpace
    from game.ship_panels import ShipModule


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
        self.modules: ShipModules = ShipModules()
        self.module_names = set()
        self.bridge_crew = [
            # TODO: placeholder for usernames of the bridge crew members
            "test",
        ]
        self.module_permissions = {}

    def add_module(self, module: ShipModule):
        setattr(self.modules, module.module_type, module)
        self.module_names.add(module.module_type)
        module.attach_to_ship(self)
