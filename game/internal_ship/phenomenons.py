from __future__ import annotations

import typing

from game.internal_ship.enums import PhenomenonState

if typing.TYPE_CHECKING:
    from game.internal_ship.classes import InternalShip


class Hypersphere:
    def __init__(self, ship: InternalShip, power: int, state: PhenomenonState.PENDING):
        print("New Hypersphere created")
        self.ship: InternalShip = ship
        self.ship.hypersphere = self
        self.power: int = power
        self.state: PhenomenonState = state
        self.simulation = self.ship.simulation
        self.simulation.phenomenons.add(self)
        self._pending_power = 0

    def tick(self):
        if self.state == PhenomenonState.PENDING:
            self.activate()
        self._add_pending_attributes()

        self.power -= 1
        if self.power <= 0:
            self.destroy()

    def power_up(self, value: int):
        self._pending_power += value

    def _add_pending_attributes(self):
        self.power += self._pending_power
        self._pending_power = 0

    def activate(self):
        print("Activating pending hypersphere")
        self.state = PhenomenonState.ACTIVE

    def destroy(self):
        self.ship.hypersphere = None
        self.ship = None
        self.state = PhenomenonState.DELETED
