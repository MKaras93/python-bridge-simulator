from __future__ import annotations
from typing import TYPE_CHECKING

from game.ship_modules import ShipModules, ShipModule

if TYPE_CHECKING:
    from game.loop import Game
    from game.hyperspace import HyperspaceShip


class PlayerShip:
    """
    Layer between server and object representing ship (in any of the spaces).

    Everything the server (so the players) do has to come through this object.
    Differences between normal npc ship and players ship are implemented here.
    """
    def __init__(self, game: Game, hyperspace_ship: HyperspaceShip):
        self.game = game
        self.space = game.space
        self.hyperspace_ship = hyperspace_ship
        self.modules = ShipModules()
        self.module_names = set()

    def add_module(self, module: ShipModule):
        setattr(self.modules, module.module_type, module)
        self.module_names.add(module.module_type)
        module.attach_to_ship(self)
