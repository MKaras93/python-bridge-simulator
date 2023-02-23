from __future__ import annotations

from enum import Enum


class SectorStateEnum(str, Enum):
    #  Note: optimization potential here, switching to int enum might reduce the cost of storing a sector.
    LOADED = "loaded"
