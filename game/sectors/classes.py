from __future__ import annotations

import typing
from enum import Enum

from pymunk import Vec2d

if typing.TYPE_CHECKING:
    from game.hyperspace.classes import HyperspaceShip
    from game.internal_ship.classes import InternalShip


class Sector:
    sectors_map = {}

    def __init__(self, position: Vec2d):
        self.ships = set()
        self.structures = set()
        self.allegiance = None
        self.position = position
        self.name = "Sector {}".format(position)
        self.state = SectorStateEnum.LOADED
        self.sectors_map[position] = self

    @classmethod
    def get_sector(cls, position: Vec2d):
        sector = cls.sectors_map.get((position.x, position.y), None)
        if not sector:
            sector = cls(position)
        return sector

    def add_ship(self, ship: HyperspaceShip):
        self.ships.add(ship)

    def remove_ship(self, ship: HyperspaceShip):
        self.ships.remove(ship)


class SectorStateEnum(str, Enum):
    #  Note: optimization potential here, switching to int enum might reduce the cost of storing a sector.
    LOADED = "loaded"


class SectorShip:
    def __init__(self, internal_ship: InternalShip, sector: Sector):
        self.internal_ship: InternalShip = internal_ship
        self.sector: Sector = sector

    def destroy(self):
        self.internal_ship.sector_ship = None
        self.internal_ship = None
        print("{} destroyed".format(self))
